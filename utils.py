# Function to check whether the transaction format is correct.
# It appends "Ignored" if the transaction format, couriers, or sizes are invalid.
def check_transaction(line, possible_sizes, possible_providers):
    parts = line.split()

    if not parts or len(parts) < 3:
        return f"{line} Ignored"

    date, size, provider = parts[:3]  

    # Check if date contains exactly 8 digits
    digits_only = ''.join(filter(str.isdigit, date))
    if len(digits_only) != 8:
        return f"{line} Ignored"
    
    # Get year and month
    year, month = digits_only[:4], digits_only[4:6]

    if size not in possible_sizes or provider not in possible_providers:
        return f"{line} Ignored"

    return (year, month, date, size, provider)


# Function to read data from input.txt
def parse_input_file(filename, possible_sizes, possible_providers):
    parsed_transactions = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            result = check_transaction(line, possible_sizes, possible_providers)
            parsed_transactions.append(result)

    return parsed_transactions
