# Discount rules module

# Rule 1: Ensure all S shipments match the lowest S package price among providers.
# Base price is not reduced here as the 10eur limit needs to be checked first.
def match_lowest_S_price(base_price, size, lowest_s_price):
    discount = 0
    if size == "S" and base_price > lowest_s_price:
        discount = base_price - lowest_s_price
    return base_price, discount

# Rule 2: The third L shipment via LP should be free, but only once a calendar month.
def free_L_shipment(year_month, provider, size, base_price, lp_L_counter):
    discount = 0 

    if provider == "LP" and size == "L":
        lp_L_counter[year_month] += 1 

        if lp_L_counter[year_month] == 3:
            discount = base_price  

    return base_price, discount

# Rule 3: Accumulated discounts cannot exceed 10 € in a calendar month.
def check_discount_limit(discount, monthly_discounts, year_month, base_price):
    remaining_discount = 10.00 - monthly_discounts[year_month]
    # If there are not enough funds to fully cover a discount this month, it is partially covered.
    if discount > remaining_discount:
        discount = remaining_discount

    base_price -= discount  
    monthly_discounts[year_month] += discount
    return base_price, discount
