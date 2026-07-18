from extract.get_flights import extract_flights
from transform.clean_flights import clean_flights
from transform.create_gold import create_gold
from load.load_postgres import load_to_postgres


def main():

    bronze_file = extract_flights()

    silver_file = clean_flights(bronze_file)

    gold_file = create_gold(silver_file)

    load_to_postgres(gold_file)


if __name__ == "__main__":
    main()