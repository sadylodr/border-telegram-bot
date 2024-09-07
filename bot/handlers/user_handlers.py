from aiogram import F, types, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.user_keyboards import (
    get_main_kb, get_main_ikb, get_lt_ikb, get_pol_ikb, get_cartype_ikb
)
from bot.response.get_response import BorderInfo

from bot.database.database import Database


router = Router()
db = Database()


@router.message(CommandStart())
async def cmd_start(msg: types.Message):
    reply_text = (
        '❗<b>Внимание!</b> Информация о количестве ТС предоставлена без учета живой очереди '
        'перед въездом в зону ожидания.❗\n\nДля того, чтобы узнать ситуацию на границе введите /stats или нажмите на кнопку снизу экрана.'
    )

    user_id = msg.from_user.id 
    username = msg.from_user.username

    if not db.user_exists(user_id):
        db.add_user(user_id, username)
        print(f"Добавлен новый пользователь: {username} ({user_id})")
    else:
        print(f"Пользователь уже существует: {username} ({user_id})")

    await msg.answer(
        text=reply_text,
        parse_mode='HTML',
        reply_markup=get_main_kb()
    )


@router.message(F.text == 'Помощь 🔎')
@router.message(Command('help'))
async def cmd_help(msg: types.Message):
    reply_text = (
        "<b>/start</b> - <em>стартовое сообщение</em>\n"
        "<b>/help</b> - <em>это сообщение</em>\n"
        "<b>/stats</b> - <em>узнать статистику о любой ЗО</em>"
    )
    await msg.answer(
        text=reply_text,
        parse_mode='HTML'
    )


@router.message(F.text == 'Актуальная информация ℹ️')
@router.message(Command('stats'))
async def cmd_stats(msg: types.Message):
    reply_text = "Выберите один из вариантов:"
    await msg.answer(
        text=reply_text,
        parse_mode='HTML',
        reply_markup=get_main_ikb()
    )


async def send_queue_info(msg: types.Message, name: str, vehicle_type: str):
    border_info = BorderInfo()
    if vehicle_type == 'Car':
        queue_info = border_info.get_car_queue(name)
    else:
        queue_info = border_info.get_truck_queue(name)
    await msg.answer(
        text=queue_info,
        parse_mode='HTML'
    )


async def send_best_queue_info(msg: types.Message, vehicle_type: str):
    border_info = BorderInfo()
    if vehicle_type == 'Car':
        queue_info = border_info.get_best_car()
    else:
        queue_info = border_info.get_best_truck()
    await msg.answer(
        text=queue_info,
        parse_mode='HTML'
    )


@router.message(F.text == 'Легковые авто Каменный лог 🚗')
@router.message(Command('kamlog_car'))
async def cmd_kamlog_car(msg: types.Message):
    await send_queue_info(msg, 'Каменный Лог', 'Car')


@router.message(F.text == 'Грузовые авто Каменный лог 🛻')
@router.message(Command('kamlog_truck'))
async def cmd_kamlog_truck(msg: types.Message):
    await send_queue_info(msg, 'Каменный Лог', 'Truck')


@router.message(F.text == 'Легковые авто Бенякони 🚗')
@router.message(Command('ben_car'))
async def cmd_ben_car(msg: types.Message):
    await send_queue_info(msg, 'Бенякони', 'Car')


@router.message(F.text == 'Грузовые авто Бенякони 🛻')
@router.message(Command('ben_truck'))
async def cmd_ben_truck(msg: types.Message):
    await send_queue_info(msg, 'Бенякони', 'Truck')


@router.message(F.text == 'Легковые авто Брест 🚗')
@router.message(Command('br_car'))
async def cmd_br_car(msg: types.Message):
    await send_queue_info(msg, 'Брест', 'Car')


@router.message(F.text == 'Грузовые авто Брест 🛻')
@router.message(Command('br_truck'))
async def cmd_br_truck(msg: types.Message):
    await send_queue_info(msg, 'Брест', 'Truck')


@router.callback_query(lambda c: c.data in ["lt", "pol", "best_border"])
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == 'lt':
        await callback_query.message.edit_text(
            'Выберите пограничный переход:', 
            reply_markup=get_lt_ikb()
        )
    elif callback_query.data == 'pol':
        await callback_query.message.edit_text(
            'Выберите пограничный переход:', 
            reply_markup=get_pol_ikb()
        )
    elif callback_query.data == 'best_border':
        await callback_query.message.edit_text(
            'Выберите вид транспорта:', 
            reply_markup=get_cartype_ikb('best')
        )
    await callback_query.answer()


@router.callback_query(lambda c: c.data in ["br", "kamlog", "ben"])
async def process_callback_second(callback_query: types.CallbackQuery):
    location_to_kb = {
        'kamlog': get_cartype_ikb('kamlog'),
        'ben': get_cartype_ikb('ben'),
        'br': get_cartype_ikb('br')
    }
    await callback_query.message.edit_text(
        'Выберите вид транспорта:', 
        reply_markup=location_to_kb[callback_query.data]
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data in [
    "car_br", "truck_br", "car_ben", "truck_ben", "car_kamlog", "truck_kamlog"
])
async def process_callback_third(callback_query: types.CallbackQuery):
    data_to_command = {
        'car_kamlog': cmd_kamlog_car,
        'truck_kamlog': cmd_kamlog_truck,
        'car_ben': cmd_ben_car,
        'truck_ben': cmd_ben_truck,
        'car_br': cmd_br_car,
        'truck_br': cmd_br_truck
    }
    command = data_to_command.get(callback_query.data)
    if command:
        await command(callback_query.message)
    await callback_query.answer()


@router.callback_query(lambda c: c.data in ["best_car", "best_truck"])
async def process_callback_best(callback_query: types.CallbackQuery):
    vehicle_type = 'Car' if callback_query.data == 'best_car' else 'Truck'
    await send_best_queue_info(callback_query.message, vehicle_type)
    await callback_query.answer()


async def on_shutdown():
    db.close()