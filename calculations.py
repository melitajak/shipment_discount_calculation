from utils import check_transaction, parse_input_file
from discount_rules import match_lowest_S_price, free_L_shipment, check_discount_limit
from constants import PRICES, POSSIBLE_SIZES, POSSIBLE_PROVIDERS

# Function to calculate shipping prices and apply rules
def calculate_shipping_price(transactions):
    lowest_s_price = min(PRICES["LP"]["S"], PRICES["MR"]["S"])
    monthly_discounts = {}  
    lp_L_counter = {}  
    processed_transactions = []

    for entry in transactions:
        # Ignore invalid transactions
        if isinstance(entry, str):  
            processed_transactions.append(entry)
            continue  

        year, month, date, size, provider = entry
        year_month = f"{year}-{month}"

        monthly_discounts.setdefault(year_month, 0) 
        lp_L_counter.setdefault(year_month, 0)

        base_price = PRICES[provider][size]

        # Apply first rule
        base_price, discount = match_lowest_S_price(base_price, size, lowest_s_price)

        # Apply second rule 
        base_price, discount_L = free_L_shipment(year_month, provider, size, base_price, lp_L_counter)
        discount += discount_L  

        # Apply third rule 
        base_price, discount = check_discount_limit(discount, monthly_discounts, year_month, base_price)

        # Result formatting
        processed_transactions.append(f"{date} {size} {provider} {base_price:.2f} {discount:.2f}" if discount > 0 else f"{date} {size} {provider} {base_price:.2f} -")

    return processed_transactions
