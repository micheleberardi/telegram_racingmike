import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import filters
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests
import button
import base64
import sys
import json

with open('Config.json') as f:
    config_data = json.load(f)


bot_token = config_data.get('bot_token')
print(bot_token)

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# DEF FOR EMOTICONS
def get_flag(country_code):
    if len(country_code) != 2:
        return ""
    offset = 127397
    return chr(ord(country_code[0].upper()) + offset) + chr(ord(country_code[1].upper()) + offset)


#MAIN MENU
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " here is some help: \n\n🔔 My information: Version: 1.00 August 21 Latest addition: BETA-VERSION \n\n  (by Michele Berardi 🐗) \n\n" \
                                        "💬 I already have a lot of capabilities: \n\n" \
                                        "🏁MotoGP -Show Current 🏁 Grand Prix or ⏱️ Qualifying results. \n" \
                                        "🏁Moto2 -Show Current 🏁 Grand Prix or ⏱️ Qualifying results. \n" \
                                        "🏁Moto3 - Show Current 🏁 Grand Prix or ⏱️ Qualifying results. \n" \
                                        "👱🏼RiderMotoGp - Show information about a 👱🏼 driver from the current season. \n " \
                                        "👱🏼RiderMoto2 - Show information about a 👱🏼 driver from the current season. \n " \
                                        "👱🏼RiderMoto3 - Show information about a 👱🏼 driver from the current season.\n " \
                                        "🏆StandingsMotoGp - Show 👱🏼 driver standings for the current season.\n " \
                                        "🏆StandingsMoto2 - Show 👱🏼 driver standings for the current season.\n " \
                                        "🏆StandingsMoto3 - Show 👱🏼 driver standings for the current season.\n "

    buttons = button.button_menu()
    await message.reply(welcome_msg, reply_markup=buttons)

def register_handlers(dp: Dispatcher):
    dp.message_handler(commands=['start', 'help'])(welcome)
    dp.message_handler(lambda message: message.text == '🏁MotoGP')(motogp_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("session_"))(event_result_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("event_"))(session_result_handler)

    dp.message_handler(lambda message: message.text == '🏁Moto2')(moto2_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto2_session_"))(moto2_event_result_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto2_event_"))(moto2_session_result_handler)

    dp.message_handler(lambda message: message.text == '🏁Moto3')(moto3_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto3_session_"))(moto3_event_result_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("mot3_event_"))(moto3_session_result_handler)

    dp.message_handler(lambda message: message.text == '🏎️ F1 Result Race')(f1_handler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("f1_event_result_race_"))(f1_event_result_handler)

    dp.message_handler(lambda message: message.text == '🏎️ F1 Result Qualifying')(f1_Qhandler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("f1_event_result_qualifying_"))(f1_event_result_Qhandler)

    dp.message_handler(lambda message: message.text == '🏎️ F1 Result Sprint Race')(f1_Shandler)
    dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("f1_event_result_sprint_"))(f1_event_result_Shandler)

    dp.message_handler(lambda message: message.text == '🏆 F1 Standings Driver')(f1_standing_driver_handler)
    dp.message_handler(lambda message: message.text == '🏆 F1 Standings Constructor')(f1_standing_constructor_handler)

    dp.message_handler(lambda message: message.text == '🏆 Standings Moto2')(f1_standing_moto2_handler)
    dp.message_handler(lambda message: message.text == '🏆 Standings Moto3')(f1_standing_moto3_handler)
    dp.message_handler(lambda message: message.text == '🏆 Standings Motogp')(f1_standing_motogp_handler)


@dp.message_handler(lambda message: message.text == '🏁MotoGP')
async def motogp_handler(message: types.Message):
    await message.reply("Fetching data...")
    print("motogp")

    # Call the API to get name and id country
    api_url = "https://racingmike.com/api/v1.0/motogp-events?token=" + config_data.get('api_token') + "&year=2023&sport=motogp"
    response = requests.get(api_url)
    data = response.json()

    welcome_msg = f"Hi {message.from_user.first_name}, select the circuit you want to see the result: \n\n"

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the events and create buttons for each event
    for event in data:
        id = event.get("id")
        name = event.get("name")
        id_country = event.get("country_iso")
        flag = get_flag(id_country)
        category_id = "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"

        button_text = f"{flag} {name}"
        button_callback_data = f"session_{id}"

        print(button_callback_data)

        inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))

    # Send the message with the inline keyboard
    await message.reply(welcome_msg, reply_markup=inline_kb)

# SECTION TO GET THE SESSIONS OF THE CIRCUIT
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("session_"))
async def event_result_handler(callback_query: types.CallbackQuery):
    print("cazpppppppppppppppppppppppppppppp")
    _, session_ = callback_query.data.split("_")
    event_id = session_
    category_id = "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"
    # Call the API to get the sessions data
    api_url = f"https://racingmike.com/api/v1.0/motogp-sessions?token=" + config_data.get('api_token') + "&eventid={event_id}&categoryid={category_id}"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the sessions and create buttons for each session
    buttons = []  # Create an empty list to store the buttons
    count = 0  # Add a counter to keep track of buttons
    for session in data:
        id = session.get("id")
        number = session.get("number","")
        name = session.get("type")
        name_session = str(name)+ "" + str(number)
        name_session = name_session.replace("None", "")
        category_id = "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"
        button_text = f"🏁 {name_session}"

        button_callback_data = f"event_{event_id}_session_{name_session}"
        print(button_callback_data)
        #inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))
        buttons.append(InlineKeyboardButton(button_text, callback_data=button_callback_data))

        count += 1
        if count % 2 == 0:
            inline_kb.row(*buttons)
            buttons.clear()
    if buttons:
        inline_kb.row(*buttons)

    # Add the buttons in the list to the inline_kb using the row() method
    #inline_kb.row(*buttons)
    # Send the message with the inline keyboard
    await callback_query.message.reply("Select a session to see the result:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("event_"))
async def session_result_handler(callback_query: types.CallbackQuery):
    print(callback_query.data)
    #callback_query = 'event_df77971c-1f58-4cbd-911f-cf2391fd57e3-SPR'
    # Extract event_id from the callback data
    _, event_id, _, name_session = callback_query.data.split("_")

    category_id = "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"

    # Call the API to get the classification data
    api_url = f"https://racingmike.com/api/v1.0/motogp-full-results?token=" + config_data.get('api_token') + "&eventid={event_id}&categoryid={category_id}&session={name_session}"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    if len(data) >= 1:
        results = ""
        for session in data:
            classification_position = session.get("classification_position","N/A")
            classification_rider_country_iso = session.get("classification_rider_country_iso")
            flag = get_flag(classification_rider_country_iso)
            classification_rider_full_name = session.get("classification_rider_full_name")
            classification_team_name = session.get("classification_team_name")
            time = session.get("time")
            gap_first = session.get("gap_first")
            average_speed = session.get("average_speed")
            #results += f"Rider Number: {classification_position}\nCountry: {flag}\nName: {classification_rider_full_name}\nTeam: {classification_team_name}\nTime: {time}\nGap to first: {gap_first}\nAverage Speed: {average_speed}\n\n"
            results += f"{classification_position} {flag} {classification_rider_full_name} ({classification_team_name}) Time:{time} Gap:{gap_first} \n"


        # Process the data and send the results to the user
        await callback_query.answer("Displaying the event results")
        await callback_query.message.reply(results)
    else:
        await callback_query.message.reply("❌ No data for this session! If this session only finished recently, please try again in a few minutes")
        return


###### MOTO2 ######
@dp.message_handler(lambda message: message.text == '🏁Moto2')
async def moto2_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get name and id country
    api_url = "https://racingmike.com/api/v1.0/motogp-events?token=" + config_data.get('api_token') + "&year=2023&sport=motogp"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    print(data)

    welcome_msg = f"Hi {message.from_user.first_name}, select the circuit you want to see the result: \n\n"

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the events and create buttons for each event
    for event in data:
        id = event.get("id")
        name = event.get("name")
        id_country = event.get("country_iso")
        flag = get_flag(id_country)
        category_id = "549640b8-fd9c-4245-acfd-60e4bc38b25c"

        button_text = f"{flag} {name}"
        button_callback_data = f"moto2_session_{id}"


        print(button_callback_data)

        inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))

    # Send the message with the inline keyboard
    await message.reply(welcome_msg, reply_markup=inline_kb)

# SECTION TO GET THE SESSIONS OF THE CIRCUIT
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto2_session_"))

async def moto2_event_result_handler(callback_query: types.CallbackQuery):
    print("cazpppppppppppppppppppppppppppppp")
    _, _, moto2_session_ = callback_query.data.split("_")

    event_id = moto2_session_
    category_id = "549640b8-fd9c-4245-acfd-60e4bc38b25c"
    # Call the API to get the sessions data
    api_url = f"https://racingmike.com/api/v1.0/motogp-sessions?token=" + config_data.get('api_token') + "&eventid={event_id}&categoryid={category_id}"
    response = requests.get(api_url)
    data = response.json()

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the sessions and create buttons for each session
    buttons = []  # Create an empty list to store the buttons
    count = 0  # Add a counter to keep track of buttons
    for session in data:
        id = session.get("id")
        number = session.get("number","")
        name = session.get("type")
        name_session = str(name)+ "" + str(number)
        name_session = name_session.replace("None", "")
        category_id = "549640b8-fd9c-4245-acfd-60e4bc38b25c"
        button_text = f"🏁 {name_session}"

        button_callback_data = f"moto2_event_{event_id}_session_{name_session}"
        print(button_callback_data)
        # inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))
        buttons.append(InlineKeyboardButton(button_text, callback_data=button_callback_data))
        count += 1
        if count % 2 == 0:
            inline_kb.row(*buttons)
            buttons.clear()
    if buttons:
        inline_kb.row(*buttons)

    # Send the message with the inline keyboard
    await callback_query.message.reply("Select a session to see the result:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto2_event_"))
async def moto2_session_result_handler(callback_query: types.CallbackQuery):
    print(callback_query.data)
    #callback_query = 'event_df77971c-1f58-4cbd-911f-cf2391fd57e3-SPR'
    # Extract event_id from the callback data
    _, _, moto2_event_, _, name_session = callback_query.data.split("_")
    print(moto2_event_)
    print("CAAAAA")

    category_id = "549640b8-fd9c-4245-acfd-60e4bc38b25c"

    # Call the API to get the classification data
    api_url = f"https://racingmike.com/api/v1.0/motogp-full-results?token=" + config_data.get('api_token') + "&eventid={moto2_event_}&categoryid={category_id}&session={name_session}"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    results = ""
    for session in data:
        classification_position = session.get("classification_position","N/A")
        classification_rider_country_iso = session.get("classification_rider_country_iso")
        flag = get_flag(classification_rider_country_iso)
        classification_rider_full_name = session.get("classification_rider_full_name")
        classification_team_name = session.get("classification_team_name")
        time = session.get("time")
        gap_first = session.get("gap_first")
        average_speed = session.get("average_speed")
        #results += f"Rider Number: {classification_position}\nCountry: {flag}\nName: {classification_rider_full_name}\nTeam: {classification_team_name}\nTime: {time}\nGap to first: {gap_first}\nAverage Speed: {average_speed}\n\n"
        results += f"{classification_position} {flag} {classification_rider_full_name} ({classification_team_name}) Time:{time} Gap:{gap_first} \n"


    # Process the data and send the results to the user
    await callback_query.answer("Displaying the event results")
    await callback_query.message.reply(results)

    ###### moto3 ######
@dp.message_handler(lambda message: message.text == '🏁moto3')
async def moto3_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get name and id country
    api_url = "https://racingmike.com/api/v1.0/motogp-events?token=" + config_data.get('api_token') + "&year=2023&sport=motogp"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    print(data)

    welcome_msg = f"Hi {message.from_user.first_name}, select the circuit you want to see the result: \n\n"

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the events and create buttons for each event
    for event in data:
        id = event.get("id")
        name = event.get("name")
        id_country = event.get("country_iso")
        flag = get_flag(id_country)
        category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"

        button_text = f"{flag} {name}"
        button_callback_data = f"moto3_session_{id}"

        print(button_callback_data)

        inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))

    # Send the message with the inline keyboard
    await message.reply(welcome_msg, reply_markup=inline_kb)

# SECTION TO GET THE SESSIONS OF THE CIRCUIT
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto3_session_"))
async def moto3_event_result_handler(callback_query: types.CallbackQuery):
    print("cazpppppppppppppppppppppppppppppp")
    _, _, moto3_session_ = callback_query.data.split("_")

    event_id = moto3_session_
    category_id = "549640b8-fd9c-4245-acfd-60e4bc38b25c"
    # Call the API to get the sessions data
    api_url = f"https://racingmike.com/api/v1.0/motogp-sessions?token=" + config_data.get('api_token') + "&eventid={event_id}&categoryid={category_id}"
    response = requests.get(api_url)
    data = response.json()

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the sessions and create buttons for each session
    buttons = []  # Create an empty list to store the buttons
    count = 0  # Add a counter to keep track of buttons
    for session in data:
        id = session.get("id")
        number = session.get("number", "")
        name = session.get("type")
        name_session = str(name) + "" + str(number)
        name_session = name_session.replace("None", "")
        category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"
        button_text = f"🏁 {name_session}"

        button_callback_data = f"moto3_event_{event_id}_session_{name_session}"
        print(button_callback_data)
        # inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))
        buttons.append(InlineKeyboardButton(button_text, callback_data=button_callback_data))

        count += 1
        if count % 2 == 0:
            inline_kb.row(*buttons)
            buttons.clear()
    if buttons:
        inline_kb.row(*buttons)

    # Send the message with the inline keyboard
    await callback_query.message.reply("Select a session to see the result:", reply_markup=inline_kb)

###standingmotogp_event_handler
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("standingmotogp_event_handler"))
async def moto3_event_result_handler(callback_query: types.CallbackQuery):
    print("cazpppppppppppppppppppppppppppppp")
    _, _, standingmotogp_event_handler = callback_query.data.split("_")

    event_id = standingmotogp_event_handler
    category_id = "549640b8-fd9c-4245-acfd-60e4bc38b25c"
    # Call the API to get the sessions data
    api_url = f"https://racingmike.com/api/v1.0/motogp-sessions?token=" + config_data.get('api_token') + "&eventid={event_id}&categoryid={category_id}"
    response = requests.get(api_url)
    data = response.json()

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the sessions and create buttons for each session
    buttons = []  # Create an empty list to store the buttons
    count = 0  # Add a counter to keep track of buttons
    for session in data:
        id = session.get("id")
        number = session.get("number", "")
        name = session.get("type")
        name_session = str(name) + "" + str(number)
        name_session = name_session.replace("None", "")
        category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"
        button_text = f"🏁 {name_session}"

        button_callback_data = f"moto3_event_{event_id}_session_{name_session}"
        print(button_callback_data)
        # inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))
        buttons.append(InlineKeyboardButton(button_text, callback_data=button_callback_data))

        count += 1
        if count % 2 == 0:
            inline_kb.row(*buttons)
            buttons.clear()
    if buttons:
        inline_kb.row(*buttons)

    # Send the message with the inline keyboard
    await callback_query.message.reply("Select a session to see the result:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("moto3_event_"))
async def moto3_session_result_handler(callback_query: types.CallbackQuery):
    print(callback_query.data)
    # callback_query = 'event_df77971c-1f58-4cbd-911f-cf2391fd57e3-SPR'
    # Extract event_id from the callback data
    _, _, moto3_event_, _, name_session = callback_query.data.split("_")
    print(moto3_event_)
    print("CAAAAA")

    category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"

    # Call the API to get the classification data
    api_url = f"https://racingmike.com/api/v1.0/motogp-full-results?token=" + config_data.get('api_token') + "&eventid={moto3_event_}&categoryid={category_id}&session={name_session}"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    if len(data) >= 1:
        results = ""
        for session in data:
            classification_position = session.get("classification_position", "N/A")
            classification_rider_country_iso = session.get("classification_rider_country_iso")
            flag = get_flag(classification_rider_country_iso)
            classification_rider_full_name = session.get("classification_rider_full_name")
            classification_team_name = session.get("classification_team_name")
            time = session.get("time")
            gap_first = session.get("gap_first")
            average_speed = session.get("average_speed")
            # results += f"Rider Number: {classification_position}\nCountry: {flag}\nName: {classification_rider_full_name}\nTeam: {classification_team_name}\nTime: {time}\nGap to first: {gap_first}\nAverage Speed: {average_speed}\n\n"
            results += f"{classification_position} {flag} {classification_rider_full_name} ({classification_team_name}) Time:{time} Gap:{gap_first} \n"

        # Process the data and send the results to the user
        await callback_query.answer("Displaying the event results")
        await callback_query.message.reply(results)
    else:
        await callback_query.message.reply(
            "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
        return

#### LIVE TIMING
@dp.message_handler(lambda message: message.text == '🏁LIVE TIMING MOTOGP')
async def livetiming_event_handler(message: types.Message):
    await message.reply("Fetching data...")
    # Call the API to get the classification data
    api_url = f"https://racingmike.com/api/v1.0/liveresult?token=" + config_data.get('api_token') + ""
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    if len(data) >= 1:
        results = ""
        for session in data:
            classification_rider_full_name = session.get("classification_rider_full_name")
            classification_position = session.get("pos", "")
            lap_time = session.get("lap_time", "")
            best_lap = session.get("last_lap_time", "")
            #lap = session.get("lap", "")
            last_lap = session.get("last_lap", "")
            #team = session.get("team_name", "")
            #bike = session.get("bike", "")
            #results += f"{classification_position}) {classification_rider_full_name} \n * LapTime:{lap_time} \n * BestLap:{best_lap} \n * LastLap:{last_lap} \n\n"
            results += f"{classification_position}) {classification_rider_full_name}  Best Lap:{best_lap}  Last Lap:{last_lap} \n\n"

        # Process the data and send the results to the user
        await message.reply("Real Time of Last Event of the day")
        await message.reply(results)
    else:
        await message.reply("❌ No data for this session! If this session only finished recently, please try again in a few minutes")
        return

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("event_33333"))
async def session_result_handler(callback_query: types.CallbackQuery):
    print(callback_query.data)
    #callback_query = 'event_df77971c-1f58-4cbd-911f-cf2391fd57e3-SPR'
    # Extract event_id from the callback data
    _, event_id, _, name_session = callback_query.data.split("_")

    category_id = "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"

    # Call the API to get the classification data
    api_url = f"https://racingmike.com/api/v1.0/motogpclassificationstotal?token=" + config_data.get('api_token') + "&eventid={event_id}&categoryid={category_id}&sessionid={name_session}"

    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    #data = {"CIRCUIT": [{"name": "MotoGP™", "circuit": "Autódromo Internacional do Algarve", "date": "2023-03-25 15:00:00", "session_type_number": "SPR", "condition_weather": "", "record_type": "bestLap", "record_rider_full_name": "Fabio Quartararo", "record_rider_country_iso": "FR", "record_best_lap_time": "01:39:00", "record_speed": 166.2, "record_year": 2022 } ], "RIDERS": [{"classification_position": 1, "classification_rider_full_name": "Francesco Bagnaia", "classification_rider_number": 1, "constructor_name": "Ducati", "classification_team_name": "Ducati Lenovo Team", "total_laps": 12, "average_speed": "166.3", "gap_first": "0.000", "gap_lap": "0", "time": "19:52.8620", "status": "INSTND", "points": "12"}, {"classification_position": 2, "classification_rider_full_name": "Jorge Martin", "classification_rider_number": 89, "constructor_name": "Ducati", "classification_team_name": "Prima Pramac Racing", "total_laps": 12, "average_speed": "166.2", "gap_first": "0.307", "gap_lap": "0", "time": "19:53.1690", "status": "INSTND", "points": "9"}, {"classification_position": 3, "classification_rider_full_name": "Marc Marquez", "classification_rider_number": 93, "constructor_name": "Honda", "classification_team_name": "Repsol Honda Team", "total_laps": 12, "average_speed": "166", "gap_first": "1.517", "gap_lap": "0", "time": "19:54.3790", "status": "INSTND", "points": "7"}, {"classification_position": 4, "classification_rider_full_name": "Jack Miller", "classification_rider_number": 43, "constructor_name": "KTM", "classification_team_name": "Red Bull KTM Factory Racing", "total_laps": 12, "average_speed": "166", "gap_first": "1.603", "gap_lap": "0", "time": "19:54.4650", "status": "INSTND", "points": "6"}, {"classification_position": 5, "classification_rider_full_name": "Maverick Viñales", "classification_rider_number": 12, "constructor_name": "Aprilia", "classification_team_name": "Aprilia Racing", "total_laps": 12, "average_speed": "166", "gap_first": "1.854", "gap_lap": "0", "time": "19:54.7160", "status": "INSTND", "points": "5"}, {"classification_position": 6, "classification_rider_full_name": "Aleix Espargaro", "classification_rider_number": 41, "constructor_name": "Aprilia", "classification_team_name": "Aprilia Racing", "total_laps": 12, "average_speed": "166", "gap_first": "2.106", "gap_lap": "0", "time": "19:54.9680", "status": "INSTND", "points": "4"}, {"classification_position": 7, "classification_rider_full_name": "Miguel Oliveira", "classification_rider_number": 88, "constructor_name": "Aprilia", "classification_team_name": "CryptoDATA RNF MotoGP Team", "total_laps": 12, "average_speed": "165.8", "gap_first": "2.940", "gap_lap": "0", "time": "19:55.8020", "status": "INSTND", "points": "3"}, {"classification_position": 8, "classification_rider_full_name": "Johann Zarco", "classification_rider_number": 5, "constructor_name": "Ducati", "classification_team_name": "Prima Pramac Racing", "total_laps": 12, "average_speed": "165.5", "gap_first": "5.595", "gap_lap": "0", "time": "19:58.4570", "status": "INSTND", "points": "2"}, {"classification_position": 9, "classification_rider_full_name": "Alex Marquez", "classification_rider_number": 73, "constructor_name": "Ducati", "classification_team_name": "Gresini Racing MotoGP", "total_laps": 12, "average_speed": "165.5", "gap_first": "5.711", "gap_lap": "0", "time": "19:58.5730", "status": "INSTND", "points": "1"}, {"classification_position": 10, "classification_rider_full_name": "Fabio Quartararo", "classification_rider_number": 20, "constructor_name": "Yamaha", "classification_team_name": "Monster Energy Yamaha MotoGP", "total_laps": 12, "average_speed": "165.4", "gap_first": "5.924", "gap_lap": "0", "time": "19:58.7860", "status": "INSTND", "points": "0"}, {"classification_position": 11, "classification_rider_full_name": "Raul Fernandez", "classification_rider_number": 25, "constructor_name": "Aprilia", "classification_team_name": "CryptoDATA RNF MotoGP Team", "total_laps": 12, "average_speed": "165.1", "gap_first": "8.160", "gap_lap": "0", "time": "20:01.0220", "status": "INSTND", "points": "0"}, {"classification_position": 12, "classification_rider_full_name": "Brad Binder", "classification_rider_number": 33, "constructor_name": "KTM", "classification_team_name": "Red Bull KTM Factory Racing", "total_laps": 12, "average_speed": "165.1", "gap_first": "8.384", "gap_lap": "0", "time": "20:01.2460", "status": "INSTND", "points": "0"}, {"classification_position": 13, "classification_rider_full_name": "Alex Rins", "classification_rider_number": 42, "constructor_name": "Honda", "classification_team_name": "LCR Honda CASTROL", "total_laps": 12, "average_speed": "164.7", "gap_first": "11.288", "gap_lap": "0", "time": "20:04.1500", "status": "INSTND", "points": "0"}, {"classification_position": 14, "classification_rider_full_name": "Franco Morbidelli", "classification_rider_number": 21, "constructor_name": "Yamaha", "classification_team_name": "Monster Energy Yamaha MotoGP", "total_laps": 12, "average_speed": "163.9", "gap_first": "17.138", "gap_lap": "0", "time": "20:10.0000", "status": "INSTND", "points": "0"}, {"classification_position": 15, "classification_rider_full_name": "Takaaki Nakagami", "classification_rider_number": 30, "constructor_name": "Honda", "classification_team_name": "LCR Honda IDEMITSU", "total_laps": 12, "average_speed": "163.8", "gap_first": "18.128", "gap_lap": "0", "time": "20:10.9900", "status": "INSTND", "points": "0"}, {"classification_position": 16, "classification_rider_full_name": "Fabio Di Giannantonio", "classification_rider_number": 49, "constructor_name": "Ducati", "classification_team_name": "Gresini Racing MotoGP", "total_laps": 12, "average_speed": "163.3", "gap_first": "21.235", "gap_lap": "0", "time": "20:14.0970", "status": "INSTND", "points": "0"}, {"classification_position": null, "classification_rider_full_name": "Luca Marini", "classification_rider_number": 10, "constructor_name": "Ducati", "classification_team_name": "Mooney VR46 Racing Team", "total_laps": 1, "average_speed": "161.1", "gap_first": "0.000", "gap_lap": "11", "time": "01:42.6100", "status": "OUTSTND", "points": "0"}, {"classification_position": null, "classification_rider_full_name": "Marco Bezzecchi", "classification_rider_number": 72, "constructor_name": "Ducati", "classification_team_name": "Mooney VR46 Racing Team", "total_laps": 2, "average_speed": "162.6", "gap_first": "0.000", "gap_lap": "10", "time": "03:23.2820", "status": "OUTSTND", "points": "0"}, {"classification_position": null, "classification_rider_full_name": "Enea Bastianini", "classification_rider_number": 23, "constructor_name": "Ducati", "classification_team_name": "Ducati Lenovo Team", "total_laps": 1, "average_speed": "161.7", "gap_first": "0.000", "gap_lap": "11", "time": "01:42.1980", "status": "OUTSTND", "points": "0"}, {"classification_position": null, "classification_rider_full_name": "Augusto Fernandez", "classification_rider_number": 37, "constructor_name": "KTM", "classification_team_name": "GASGAS Factory Racing Tech3", "total_laps": 0, "average_speed": "0", "gap_first": "0.000", "gap_lap": "0", "time": "", "status": "NOTFINISHFIRST", "points": "0"}, {"classification_position": null, "classification_rider_full_name": "Joan Mir", "classification_rider_number": 36, "constructor_name": "Honda", "classification_team_name": "Repsol Honda Team", "total_laps": 0, "average_speed": "0", "gap_first": "0.000", "gap_lap": "0", "time": "", "status": "NOTFINISHFIRST", "points": "0"} ] }
    if len(data) >= 1:
        results = ""
        results+=f"🏁CATEGORY :{data[0].get('name')}\n📍CIRCUIT :{data[0].get('circuit')}\n📅DATE :{data[0].get('date')}\n SESSION :{data[0].get('session_type_number')}\n RECORD TYPE :{data[0].get('record_type')}\n RECORD RIDER FULL NAME :{data[0].get('record_rider_full_name')}\n RECORD RIDER TEAM NAME :{data[0].get('record_rider_country_iso')}\n RECORD RIDER TIME :{data[0].get('record_best_lap_time')}\n RECORD RIDER AVERAGE SPEED :{data[0].get('record_speed')}\n RECORD YEAR :{data[0].get('record_year')}\n\n"
        for session in data:
            classification_position = session.get("classification_position","N/A")
            classification_rider_number = session.get("classification_rider_number","N/A")
            classification_rider_number = session.get("classification_rider_number","N/A")
            constructor_name = session.get("classification_team_name","N/A")
            total_laps = session.get("total_laps","N/A")
            average_speed = session.get("average_speed","N/A")
            gap_first = session.get("gap_first","N/A")
            gap_lap = session.get("gap_lap","N/A")
            time = session.get("time","N/A")
            status = session.get("status","N/A")
            points = session.get("points","N/A")
            results += f"🥇{classification_position}\n🏁{classification_rider_number}\n🏆{constructor_name}\n🏁{total_laps}\n🏆{average_speed}\n🏁{gap_first}\n🏆{gap_lap}\n🏁{time}\n🏆{status}\n🏁{points}\n\n"


        # Process the data and send the results to the user
        result = results.replace(null, "N/A")
        await callback_query.answer("Displaying the event results")
        await callback_query.message.reply(results)
    else:
        await callback_query.message.reply("❌ No data for this session! If this session only finished recently, please try again in a few minutes")
        return


##### FORMULA ONE SECTION #####
@dp.message_handler(lambda message: message.text == '🏎️ F1 Race Result')
async def f1_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get name and id country
    api_url = "https://racingmike.com/api/v1.0/f1-circuits?token=" + config_data.get('api_token') + "&year=2023"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    print(data)

    welcome_msg = f"Hi {message.from_user.first_name}, select the circuit you want to see the result: \n\n"

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the events and create buttons for each event
    for event in data:
        id = event.get("raceId")
        name = event.get("name")
        round = event.get("round")
        #flag = get_flag(id_country)
        #category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"

        button_text = f"{name}"
        button_callback_data = f"f1_event_result_race_{round}"

        print(button_callback_data)

        inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))

    # Send the message with the inline keyboard
    await message.reply(welcome_msg, reply_markup=inline_kb)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("f1_event_result_race_"))
async def f1_event_result_handler(callback_query: types.CallbackQuery):
    print("cazpppppppppppppppppppppppppppppp")
    print(callback_query.data)
    #sys.exit(0)
    f1_event_result_race_ = callback_query.data.split("_")

    roundnumber = f1_event_result_race_[4]
    #roundnumber = 9
    print(roundnumber)
    #sys.exit(0)
    api_url = f"https://racingmike.com/api/v1.0/f1-result-races?token=" + config_data.get('api_token') + "&year=2023&roundnumber={roundnumber}"
    response = requests.get(api_url)
    data = response.json()
    if len(data) >= 1:
        results = ""
        for session in data:
            id = session.get("id")
            fullname = session.get("fullname", "")
            position = session.get("position")
            flag = session.get("flag")
            team = session.get("team")
            time = session.get("time")
            fastestLap = session.get("fastestLap")
            fastestLapSpeed = session.get("fastestLapSpeed")
            points = session.get("points")
            results += f"({position}) {flag} {fullname} {team} {time} \nFastlap: {fastestLap} \nFastlapSpeed:{fastestLapSpeed} \nPoints:{points}\n\n"

        # Process the data and send the results to the user
        #result = results.replace(null, "N/A")
        await callback_query.answer("Displaying the event results")
        await callback_query.message.reply(results)
    else:
        await callback_query.message.reply(
            "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
        return


@dp.message_handler(lambda message: message.text == '🏎️ F1 Result Qualifying')
async def f1_Qhandler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get name and id country
    api_url = "https://racingmike.com/api/v1.0/f1-circuits?token=" + config_data.get('api_token') + "&year=2023"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    print(data)

    welcome_msg = f"Hi {message.from_user.first_name}, select the circuit you want to see the result: \n\n"

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the events and create buttons for each event
    for event in data:
        id = event.get("raceId")
        name = event.get("name")
        round = event.get("round")
        #flag = get_flag(id_country)
        #category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"

        button_text = f"{name}"
        button_callback_data = f"f1_event_result_qualifying_{round}"

        print(button_callback_data)

        inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))

    # Send the message with the inline keyboard
    await message.reply(welcome_msg, reply_markup=inline_kb)



@dp.message_handler(lambda message: message.text == '🏎️ F1 Result Sprint Race')
async def f1_Shandler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get name and id country
    api_url = "https://racingmike.com/api/v1.0/f1-circuits-sprint?token=" + config_data.get('api_token') + "&year=2023"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    print(data)

    welcome_msg = f"Hi {message.from_user.first_name}, select the circuit you want to see the result: \n\n"

    # Create InlineKeyboardMarkup
    inline_kb = InlineKeyboardMarkup()

    # Loop through the events and create buttons for each event
    for event in data:
        id = event.get("raceId")
        name = event.get("name")
        round = event.get("round")
        #flag = get_flag(id_country)
        #category_id = "954f7e65-2ef2-4423-b949-4961cc603e45"

        button_text = f"{name}"
        button_callback_data = f"f1_event_result_sprint_{round}"

        print(button_callback_data)

        inline_kb.add(InlineKeyboardButton(button_text, callback_data=button_callback_data))

    # Send the message with the inline keyboard
    await message.reply(welcome_msg, reply_markup=inline_kb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("f1_event_result_qualifying_"))
async def f1_event_result_Qhandler(callback_query: types.CallbackQuery):
    print("cazpppppppppppppppppppppppppppppp")
    print(callback_query.data)
    # sys.exit(0)
    f1_event_result_qualifying_ = callback_query.data.split("_")

    roundnumber = f1_event_result_qualifying_[4]
    # roundnumber = 9
    print(roundnumber)
    # sys.exit(0)
    api_url = f"https://racingmike.com/api/v1.0/f1-result-qualifying?token=" + config_data.get('api_token') + "&year=2023&roundnumber={roundnumber}"
    response = requests.get(api_url)
    data = response.json()
    if len(data) >= 1:
        results = ""
        for session in data:
            id = session.get("id")
            fullname = session.get("fullname", "")
            position = session.get("position")
            flag = session.get("flag")
            team = session.get("team")
            q1 = session.get("q1")
            q2 = session.get("q2")
            q3 = session.get("q3")

            results += f"🥇{position} {flag} {fullname} {team} \nQ1: {q1} \nQ2: {q2} \nQ3: {q3}\n\n"

        # Process the data and send the results to the user
        # result = results.replace(null, "N/A")
        await callback_query.answer("Displaying the event results")
        await callback_query.message.reply(results)
    else:
        await callback_query.message.reply(
            "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
        return


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("f1_event_result_sprint_"))
async def f1_event_result_Shandler(callback_query: types.CallbackQuery):
    print("ZZZZZZZZZZOOOO")
    print(callback_query.data)
    # sys.exit(0)
    f1_event_result_qualifying_ = callback_query.data.split("_")

    roundnumber = f1_event_result_qualifying_[4]
    # roundnumber = 9
    print(roundnumber)
    # sys.exit(0)
    api_url = f"https://racingmike.com/api/v1.0/f1-result-sprint?token=" + config_data.get('api_token') + "&year=2023&roundnumber={roundnumber}"
    response = requests.get(api_url)
    data = response.json()
    print(data)
    if len(data) >= 1 :
        results = ""
        for session in data:
            id = session.get("id")
            print(id)
            fullname = session.get("fullname", "")
            position = session.get("position")
            flag = session.get("flag")
            team = session.get("team")
            time = session.get("time")
            fastestLap = session.get("fastestLap")
            points = session.get("points")
            results += f"{position} {flag} {fullname} {team} {time} \nFastlap: {fastestLap} \nPoints:{points}\n\n"

        # Process the data and send the results to the user
        # result = results.replace(null, "N/A")
        print("IO SONO " +str(results))
        if id == None:
            await callback_query.answer("Displaying the event results")
            await callback_query.message.reply(results)
        else:
            await callback_query.message.reply(
                 "❌ No data for Spring Race! If this session only finished recently, please try again in a few minutes")
    else:
        await callback_query.message.reply(
            "❌ No data for Spring Race! If this session only finished recently, please try again in a few minutes")
        return


@dp.message_handler(lambda message: message.text == '🏆F1 Standings Driver')
async def f1_standing_driver_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get the F1 standings data
    api_url = "https://racingmike.com/api/v1.0/f1-driverstandings?token=" + config_data.get('api_token') + "&year=2023"
    response = requests.get(api_url)
    data = response.json()

    # Create the message with the F1 standings
    standings_msg = "🏆 F1 Standings - Drivers\n\n"
    for driver in data:
        pos = driver.get("pos")
        forename = driver.get("forename")
        surname = driver.get("surname")
        points = driver.get("points")
        nationality = driver.get("nationality")
        url = driver.get("url")

        driver_info = f"{pos}. 👨{forename} {surname} ({nationality}) 🥇{points} points\n"
        standings_msg += driver_info

    # Send the F1 standings message to the Telegram chat
    await message.reply(standings_msg)

# Assuming you have already defined the necessary configurations and handlers

# Register the handler for the button press
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'f1_standing_driver')
async def handle_f1_standing_driver_callback(callback_query: types.CallbackQuery):
    await f1_standing_driver_handler(callback_query.message)

@dp.message_handler(lambda message: message.text == '🏆F1 Standings Constructor')
async def f1_standing_constructor_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get the F1 standings data
    api_url = "https://racingmike.com/api/v1.0/f1-constructorstandings?token=" + config_data.get('api_token') + "&year=2023"
    response = requests.get(api_url)
    data = response.json()

    # Create the message with the F1 standings
    standings_msg = "🏆 F1 Constructor\n\n"
    for driver in data:
        pos = driver.get("position")
        constructorName = driver.get("constructorName")
        nationality = driver.get("constructorNationality")
        points = driver.get("points")
        url = driver.get("url")

        driver_info = f"{pos} 🏎️{constructorName} ({nationality}) 🥇{points} points\n"
        standings_msg += driver_info

    # Send the F1 standings message to the Telegram chat
    await message.reply(standings_msg)

# Assuming you have already defined the necessary configurations and handlers

# Register the handler for the button press
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'f1_standing_constructor_handler')
async def handle_f1_standing_driver_callback(callback_query: types.CallbackQuery):
    await f1_standing_driver_handler(callback_query.message)

@dp.message_handler(lambda message: message.text == '🏆Standings Moto2')
async def f1_standing_moto2_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get the F1 standings data
    api_url = "https://racingmike.com/api/v1.0/motogp-world-standing-riders?token=" + config_data.get('api_token') + "&year=2023&categoryid=549640b8-fd9c-4245-acfd-60e4bc38b25c"
    response = requests.get(api_url)
    data = response.json()

    # Create the message with the F1 standings
    standings_msg = "🏆 Moto2\n\n"
    limit = 25  # Set the limit to 25 drivers
    for i, driver in enumerate(data[:limit], start=1):
        pos = driver.get("classification_position")
        constructorName = driver.get("classification_rider_full_name")
        nationality = driver.get("classification_rider_country_iso")
        points = driver.get("total_points")
        team = driver.get("classification_team_name")

        driver_info = f"👨{constructorName} ({nationality}) 🏍️Team: {team} 🥇Points {points}\n"
        standings_msg += driver_info

    # Send the F1 standings message to the Telegram chat
    await message.reply(standings_msg)

# Assuming you have already defined the necessary configurations and handlers

# Register the handler for the button press
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'f1_standing_moto2_handler')
async def handle_f1_standing_driver_callback(callback_query: types.CallbackQuery):
    await f1_standing_driver_handler(callback_query.message)


@dp.message_handler(lambda message: message.text == '🏆Standings Moto3')
async def f1_standing_moto3_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get the F1 standings data
    api_url = "https://racingmike.com/api/v1.0/motogp-world-standing-riders?token=" + config_data.get('api_token') + "&year=2023&categoryid=954f7e65-2ef2-4423-b949-4961cc603e45"
    response = requests.get(api_url)
    data = response.json()

    # Create the message with the F1 standings
    standings_msg = "🏆 Moto3\n\n"
    limit = 25  # Set the limit to 25 drivers
    for i, driver in enumerate(data[:limit], start=1):
        pos = driver.get("classification_position")
        constructorName = driver.get("classification_rider_full_name")
        nationality = driver.get("classification_rider_country_iso")
        points = driver.get("total_points")
        team = driver.get("classification_team_name")

        driver_info = f"👨{constructorName} ({nationality}) 🏍️Team: {team} 🥇Points {points}\n"
        standings_msg += driver_info

    # Send the F1 standings message to the Telegram chat
    await message.reply(standings_msg)

# Assuming you have already defined the necessary configurations and handlers

# Register the handler for the button press
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'f1_standing_moto3_handler')
async def handle_f1_standing_driver_callback(callback_query: types.CallbackQuery):
    await f1_standing_driver_handler(callback_query.message)

@dp.message_handler(lambda message: message.text == '🏆 Standings MotoGP')
async def f1_standing_motogp_handler(message: types.Message):
    await message.reply("Fetching data...")

    # Call the API to get the F1 standings data
    api_url = "https://racingmike.com/api/v1.0/motogp-world-standing-riders?token=" + config_data.get('api_token') + "&year=2023&categoryid=e8c110ad-64aa-4e8e-8a86-f2f152f6a942"
    response = requests.get(api_url)
    data = response.json()

    # Create the message with the F1 standings
    standings_msg = "🏆 MotoGP\n\n"
    limit = 25  # Set the limit to 25 drivers
    for i, driver in enumerate(data[:limit], start=1):
        pos = driver.get("classification_position")
        constructorName = driver.get("classification_rider_full_name")
        nationality = driver.get("classification_rider_country_iso")
        points = driver.get("total_points")
        team = driver.get("classification_team_name")

        driver_info = f"👨{constructorName} ({nationality}) 🏍️Team: {team} 🥇Points {points}\n"
        standings_msg += driver_info

    # Send the F1 standings message to the Telegram chat
    await message.reply(standings_msg)

# Assuming you have already defined the necessary configurations and handlers

# Register the handler for the button press
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'f1_standing_motogp_handler')
async def handle_f1_standing_driver_callback(callback_query: types.CallbackQuery):
    await f1_standing_driver_handler(callback_query.message)


if __name__ == '__main__':
    from aiogram import executor

    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
