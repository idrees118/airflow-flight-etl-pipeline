import json
from datetime import datetime
from pathlib import Path

import requests

BRONZE_PATH = Path("/opt/airflow/data/bronze")
BRONZE_PATH.mkdir(parents=True, exist_ok=True)


def extract_flights():
    url = "https://opensky-network.org/api/states/all"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = BRONZE_PATH / f"flights_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved file: {file_path}")

    return str(file_path)


if __name__ == "__main__":
    extract_flights()