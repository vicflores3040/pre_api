import json


class AccommodationService:
    def __init__(self, data_file):
        with open(data_file, "r", encoding="utf-8") as file:
            self.accommodations = json.load(file)

    def get_accommodation(self, id):
        try:
            for accommodation in self.accommodations:
                if accommodation["id"] == id:
                    return accommodation
            return None
        except Exception as e:
            raise e
