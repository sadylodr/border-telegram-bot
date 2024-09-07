from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_main_kb():
    help_btn = KeyboardButton(text='Помощь 🔎')
    car_btn = KeyboardButton(text='Актуальная информация ℹ️')
    #analitics_btn = KeyboardButton(text='Подробная аналитика')
    #insites_btn = KeyboardButton(text='Интересные инсайты')
    
    kb = ReplyKeyboardMarkup(keyboard=[[car_btn], [help_btn]], resize_keyboard=True)
    
    return kb

def get_main_ikb():
    lt_btn = InlineKeyboardButton(text='Литва 🇱🇹', callback_data='lt')
    pol_btn = InlineKeyboardButton(text = 'Польша 🇵🇱', callback_data='pol')
    best_border_btn = InlineKeyboardButton(text='Граница с мин. очередью 🏆', callback_data='best_border')

    ikb = InlineKeyboardMarkup(inline_keyboard=[[lt_btn, pol_btn], [best_border_btn]])

    return ikb

def get_lt_ikb():
    kamenii_log_btn = InlineKeyboardButton(text='1️⃣ Каменный лог', callback_data='kamlog')
    benyakoni_btn = InlineKeyboardButton(text='2️⃣ Бенякони', callback_data='ben')
    
    lt_options = InlineKeyboardMarkup(inline_keyboard=[[kamenii_log_btn, benyakoni_btn]])

    return lt_options

def get_pol_ikb():
    brest_btn = InlineKeyboardButton(text='1️⃣ Брест', callback_data='br')

    pol_options = InlineKeyboardMarkup(inline_keyboard=[[brest_btn]])

    return pol_options


def get_cartype_ikb(location):
    if location == 'best':
        car_btn = InlineKeyboardButton(text='Легковые авто 🚗', callback_data='best_car')
        truck_btn = InlineKeyboardButton(text='Грузовые авто 🛻', callback_data='best_truck')
    elif location == 'br':
        car_btn = InlineKeyboardButton(text='Легковые авто 🚗', callback_data=f'car_{location}')
        cartype_options = InlineKeyboardMarkup(inline_keyboard=[[car_btn]])
        return cartype_options
    else:
        car_btn = InlineKeyboardButton(text='Легковые авто 🚗', callback_data=f'car_{location}')
        truck_btn = InlineKeyboardButton(text='Грузовые авто 🛻', callback_data=f'truck_{location}')
    
    cartype_options = InlineKeyboardMarkup(inline_keyboard=[[car_btn, truck_btn]])
    return cartype_options 
