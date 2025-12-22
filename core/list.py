import json
import os

class ShowData:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def show_data(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            for i, j in item.items():
                print(i, j)
