import os
import csv
import datetime as dt

from collections import defaultdict

from .settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_dict = defaultdict(int)

    def process_item(self, item, spider):
        status = item['status']
        self.status_dict[status] = self.status_dict.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        time_format = dt.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = os.path.join(
            BASE_DIR,
            'results',
            ('status_summary_'
             f'{time_format}.csv')
        )
        total = sum(self.status_dict.values())
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Статус', 'Количество'))
            writer.writerows(self.status_dict.items())
            writer.writerow(('Total', total))
