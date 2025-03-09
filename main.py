from utils import parse_input_file
from calculations import calculate_shipping_price
from constants import POSSIBLE_SIZES, POSSIBLE_PROVIDERS

def main():
    input_file = "input.txt"

    parsed_data = parse_input_file(input_file, POSSIBLE_SIZES, POSSIBLE_PROVIDERS)
    final_output = calculate_shipping_price(parsed_data)

    for entry in final_output:
        print(entry)

if __name__ == "__main__":
    main()
