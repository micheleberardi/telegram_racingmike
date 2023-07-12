from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def button_menu():
    keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add("🏁MotoGP", "🏁Moto2", "🏁Moto3")
                                                                                       #"👱🏼RiderMotoGP",
                                                                                      # "👱🏼RiderMoto2",
                                                                                      # "👱🏼RiderMoto3",
                                                                                      # "🏆StandingsMotoGP",
                                                                                      # "🏆StandingsMoto2",
                                                                                      # "🏆StandingsMoto3")
    return keyboard1


def button_menu():
    buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    buttons.add(KeyboardButton('🏁MotoGP'), KeyboardButton('🏁Moto2'), KeyboardButton('🏁Moto3'))
    buttons.add(KeyboardButton('🏆 Standings MotoGP'), KeyboardButton('🏆 Standings Moto2'), KeyboardButton('🏆 Standings Moto3'))
    buttons.add(KeyboardButton('🏎️ F1 Result Race'), KeyboardButton('🏎️ F1 Result Qualifying'),KeyboardButton('🏎️ F1 Result Sprint Race'))
    buttons.add(KeyboardButton('🏆 F1 Standings Driver'), KeyboardButton('🏆 F1 Standings Constructor'))

    return buttons