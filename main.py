import asyncio
import logging
import os
import sys

import schedule
import requests
import time

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types

from bot.handlers.user_handlers import router
from bot.database.database import Database


async def fetch_statistics(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

async def fetch_checkpoint_data():
    url = 'https://belarusborder.by/info/checkpoint?token=bts47d5f-6420-4f74-8f78-42e8e4370cc4'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['result']
        return data
    except requests.RequestException as e:
        print(f"Error fetching checkpoint data: {e}")
        return None

async def save_statistics(db, url, checkpoint_name):
    data = await fetch_statistics(url)
    
    if data is not None:
        car_last_hour = data.get('carLastHour')
        car_last_day = data.get('carLastDay')
        truck_last_hour = data.get('truckLastHour')
        truck_last_day = data.get('truckLastDay')
        
        checkpoint_data = await fetch_checkpoint_data()

        countCar = 0
        countTruck = 0

        if checkpoint_data:
            for checkpoint in checkpoint_data:
                if checkpoint['name'] == checkpoint_name:
                    countCar = checkpoint['countCar']
                    countTruck = checkpoint['countTruck']
                    break

        db.add_statistics(checkpoint_name, car_last_hour, car_last_day, truck_last_hour, truck_last_day, countCar, countTruck)
        
        print(f"Данные успешно сохранены {checkpoint_name}: {car_last_hour} машин за последний час, {car_last_day} машин за последние сутки.")
        print(f"Данные успешно сохранены {checkpoint_name}: {truck_last_hour} грузовых машин за последний час, {truck_last_day} грузовых машин за последние сутки.")
    else:
        print("Не удалось получить данные для сохранения.")

def job_hourly(db, links):
    for link, name in links:
        asyncio.create_task(save_statistics(db, link, name))


async def scheduler(db, links):
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    load_dotenv('.env')

    token = os.getenv('API_KEY')
    bot = Bot(token=token)
    dp = Dispatcher()

    db = Database()
    print('База данных запущена.')

    dp.include_router(router)


    links = [
        ('https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=b60677d4-8a00-4f93-a781-e129e1692a03', 'Каменный Лог'),
        ('https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=53d94097-2b34-11ec-8467-ac1f6bf889c0', 'Бенякони'),
        ('https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=a9173a85-3fc0-424c-84f0-defa632481e4', 'Брест')
    ]
    

    schedule.every().hour.at(":00").do(job_hourly, db, links)

    asyncio.create_task(scheduler(db, links))

    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print('There is an exception')
    finally:
        db.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n\nSuccessfully stopped.')