from AlbionOnlineData.Items import Items
import requests
from datetime import datetime
from datetime import timedelta
import Errors


class MarketData:
    albion_API_URL = "https://www.albion-online-data.com/api/v2/stats/charts"

    def __init__(self, location: str = ""):
        today = datetime.today()
        self._start_datetime = datetime(today.year, today.month, today.day, 0)
        self._final_datetime = datetime(today.year, today.month, today.day, 23)

        self.location = location

        resp = requests.get(self.albion_API_URL + '/ping')
        if resp.status_code != 200:
            raise Errors.ConnectionFailure(f"Failure to connect with the API <{self.albion_API_URL}>")

    def define_period(self, start_datetime: datetime, final_datetime: datetime):
        if final_datetime >= start_datetime:
            self._start_datetime = start_datetime
            self._final_datetime = final_datetime
        else:
            raise Errors.InvalidParameter("Start date is higher than final date")

    def get_sell_order(self, item_descriptor: str, qualities: int = 0):

        current_datetime = self._start_datetime

        sell_orders = {}

        while current_datetime < self._final_datetime:
            date = current_datetime.strftime("%m-%d-%Y")

            end_point = f"{self.albion_API_URL}/{item_descriptor}?" \
                        f"qualities={qualities}&" \
                        f"locations={self.location}&" \
                        f"date={date}&" \
                        f"time-scale=1"

            resp = requests.get(end_point)
            if resp.status_code != 200:
                raise Errors.ConnectionFailure(f"Failure to connect with the API <{self.albion_API_URL}>")
            else:
                resp = resp.json()
                full_sell_orders = self._read_sell_order_json(resp)

                city_keys = full_sell_orders.keys()
                for city in city_keys:
                    sell_orders.update({city: []})
                    city_sell_orders = full_sell_orders[city]
                    for sell_order in city_sell_orders:
                        if self._start_datetime < sell_order['datetime'] < self._final_datetime:
                            if sell_order not in sell_orders[city]:
                                sell_orders[city].append(sell_order)

            current_datetime += timedelta(days=1)

        return sell_orders

    @staticmethod
    def _read_sell_order_json(json) -> dict:
        sell_order = {}
        if len(json) > 0:
            for json_element in json:
                if 'data' in json_element:
                    location = json_element['location']
                    sell_order.update({location: []})

                    data = json_element['data']
                    timestamps = data['timestamps']
                    item_count = data['item_count']
                    prices_avg = data['prices_avg']
                    api_elements = zip(timestamps, prices_avg, item_count)

                    for timestamps, price, count in api_elements:
                        timestamps_splited = timestamps.split('T')
                        date_splited = timestamps_splited[0].split('-')
                        year = int(date_splited[0])
                        month = int(date_splited[1])
                        day = int(date_splited[2])

                        time = timestamps_splited[1]
                        hour = int(time.split(':')[0])

                        sell_datetime = datetime(year, month, day, hour)

                        sell_order[location].append(
                            {
                                'datetime': sell_datetime,
                                'price': price,
                                'count': count
                             }
                        )

        return sell_order

