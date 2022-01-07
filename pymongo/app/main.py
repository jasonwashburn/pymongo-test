import itertools
import os
import random
import string
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Dict, List

from rich import print as rprint

from pymongo import MongoClient

username = urllib.parse.quote_plus(os.environ["MONGO_INITDB_ROOT_USERNAME"])
password = urllib.parse.quote_plus(os.environ["MONGO_INITDB_ROOT_PASSWORD"])
MONGO_HOST = "mongodb"
# client = MongoClient('mongodb://%s:%s@mongodb' % (username, password))
client = MongoClient(f"mongodb://{username}:{password}@{MONGO_HOST}")

db = client["tarp-data"]
collection = db["tarp-params"]


@dataclass
class ModelDataSiteParam:
    station: str
    valid_time: int
    parameter: str
    level: int
    current_value: float
    models: Dict[Any, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "station": self.station,
            "valid_time": self.valid_time,
            "parameter": self.parameter,
            "level": self.level,
            "current_value": self.current_value,
            "models": {"GALWEM": [{"run": 1641556800, "value": self.current_value}]},
        }
        return result


def generate_single_records(num_records: int) -> List:
    rprint(f"Generating {num_records} records...")
    start = time.perf_counter()
    generated_records = []
    for _ in range(num_records):
        station_id = generate_random_station_id()
        valid_time = 1641556800
        parameter = "temperature"
        level = 1000
        current_value = random.randint(250, 325)

        record = ModelDataSiteParam(
            station_id, valid_time, parameter, level, current_value
        )
        generated_records.append(record.to_dict())
    time_to_generate = time.perf_counter() - start
    rprint(
        f"Generated {len(generated_records)} records in {time_to_generate:.2f} seconds"
    )
    return generated_records


def generate_random_station_id() -> str:
    letters = string.ascii_uppercase
    site_id = "".join(random.choice(letters) for i in range(4))
    return site_id


def main():
    num_stations = int(input("Enter number of stations: "))
    num_sfc_params = int(input("Enter number of sfc params per station: "))
    num_ua_params = int(input("Enter number of upper air params per station: "))
    num_ua_levels = int(input("Enter number of upper air levels per param: "))
    num_records = num_stations * (num_sfc_params + (num_ua_params * num_ua_levels))
    generated_records = generate_single_records(num_records)

    rprint(f"(insert_many) - Inserting {len(generated_records)} into mongo database...")
    start = time.perf_counter()
    insert_result = collection.insert_many(generated_records)
    rprint(f"Inserted records in {time.perf_counter() - start:.2f} seconds.")

    # rprint(f"(insert_one) - Inserting {len(generated_records)} into mongo database...")
    # start = time.perf_counter()
    # iter_obj = itertools.cycle(generated_records)
    # print(type(iter_obj))
    # count = 0
    # while count < len(generated_records):
    #     collection.insert_one(next(iter_obj))
    #     count += 1
    # rprint(f"Inserted records in {time.perf_counter() - start:.2f} seconds.")

    return None


if __name__ == "__main__":
    main()
