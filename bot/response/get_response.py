import requests
import datetime

class BorderInfo:
    def __init__(self):
        self.url = 'https://belarusborder.by/info/checkpoint?token=bts47d5f-6420-4f74-8f78-42e8e4370cc4'
        self.valid_checkpoints_car = ["Брест", "Бенякони", "Каменный Лог"]
        self.valid_checkpoints_truck = ['Бенякони', 'Каменный Лог']

    def _fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()['result']
        except requests.RequestException as e:
            print(f'Произошла ошибка при запросе данных: {e}')
            return None

    def _get_queue_info(self, name, vehicle_type):
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M')
        data = self._fetch_data()

        if data is None:
            return None

        for checkpoint in data:
            if checkpoint['name'] == name:
                count = checkpoint[f'count{vehicle_type}']
                return (
                    f"<b>{name}</b>: На <b>{current_time}</b> количество {'легковых' if vehicle_type == 'Car' else 'грузовых'} авто\n\n"
                    f"\t\t⚠️ только в зоне ожидания - <b>{count}</b>\n"
                    f"\t\t⏳ направлено за последний час в ПП - <b>{count}</b>\n"
                    f"\t\t🕓 направлено за последний 24 часа в ПП - <b>{count}</b>\n\n"
                    "<em><b>Имейте в виду!</b> Это только количество машин в зоне ожидания. ⚠️</em>"
                )

        print(f'Контрольный пункт {name} не найден.')
        return None

    def get_car_queue(self, name):
        return self._get_queue_info(name, 'Car')

    def get_truck_queue(self, name):
        return self._get_queue_info(name, 'Truck')

    def _get_best_queue(self, valid_checkpoints, vehicle_type):
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M')
        data = self._fetch_data()

        if data is None:
            return None

        min_count = None
        best_checkpoint = None

        for checkpoint in data:
            if checkpoint['name'] in valid_checkpoints:
                count = checkpoint[f'count{vehicle_type}']
                if min_count is None or count < min_count:
                    min_count = count
                    best_checkpoint = checkpoint

        if best_checkpoint:
            return (
                f"На <b>{current_time}</b> самая маленькая очередь "
                f"{'легковых' if vehicle_type == 'Car' else 'грузовых'} машин в пограничном переходе "
                f"<b>{best_checkpoint['name']}</b>: <b>{min_count}</b>."
            )
        return 'Подходящий контрольный пункт не найден.'

    def get_best_car(self):
        return self._get_best_queue(self.valid_checkpoints_car, 'Car')

    def get_best_truck(self):
        return self._get_best_queue(self.valid_checkpoints_truck, 'Truck')
