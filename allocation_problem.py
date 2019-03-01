import random
import sys

from sympy import solve, symbols


def pretty_print(d, indent=0):
    for key1, value in d.items():
        if isinstance(value, dict):
            print('\t' * indent + str(key1))
            pretty_print(value, indent + 1)
        else:
            print('\t' * indent + str(key1) + " : " + str(value))


i = 5  # buyers
j = 9  # sellers
# Modeled as 1/x

buyer_func_coefficients = []

# the buyer functions are linear, so only taking m and c

seller_func_coefficients_k1 = []

buyer_total_requirements = []
energy_seller_max_quantity = []

for x in range(0, i):
    buyer_total_requirements.append(random.randint(5, 9))

# Sort in descending order. Giving Higher preference to buyer buying more quantity, as
# he would pay more, and hence more profit for auctioneer in terms of commission

buyer_total_requirements.sort(reverse=True)

# Take buyer function coefficients now

for x in range(0, i):
    buyer_func_coefficients.append(float(random.randint(350, 500)) / 50)

print("Buyer Requirement Set\n")
print(buyer_total_requirements)
print("\n\n=======================\n\n")
print("Buyer Utility Function Coefficients\n")
print(buyer_func_coefficients)

for x in range(0, j):
    energy_seller_max_quantity.append(random.randint(5, 15))
    seller_func_coefficients_k1.append(float(random.randint(1, 50)) / 50)

print("\n\n\nSeller Max Saleable Quantity Set\n")
print(energy_seller_max_quantity)
print("\n\n=======================\n\n")
print("Seller Utility Function Coefficients\n")
print(seller_func_coefficients_k1)

# Quantity Variable
t = symbols("t")
allocation_result = {}

# Stop Flag if all sellers are exhausted
flag = 0

for x in range(0, i):
    # buyer_solution_values = []
    price_to_be_paid = []
    dict_price_vs_index = {}
    quantity_to_be_bought = []
    current_buyer_func_coefficient = buyer_func_coefficients[x]
    # Solve expressions of all sellers w.r.t this buyer.
    for y in range(0, j):
        current_seller_coefficient = seller_func_coefficients_k1[y]
        solution = solve(current_seller_coefficient * (t ** 2) - current_buyer_func_coefficient / t, t)
        # print(solution[0])
        # buyer_solution_values.append(solution[0])
        quantity_to_be_bought.append(int(round(solution[0])))
        price_to_be_paid.append(current_buyer_func_coefficient / solution[0])
        dict_price_vs_index[price_to_be_paid[y]] = y

    while buyer_total_requirements[x] > 0:
        min_seller_index = dict_price_vs_index[min(price_to_be_paid)]
        bought = 0
        if energy_seller_max_quantity[min_seller_index] == 0:
            price_to_be_paid[min_seller_index] = 1000
            continue
        if energy_seller_max_quantity[min_seller_index] > quantity_to_be_bought[min_seller_index]:
            bought = quantity_to_be_bought[min_seller_index]
        else:
            bought = energy_seller_max_quantity[min_seller_index]

        if bought > buyer_total_requirements[x]:
            bought = buyer_total_requirements[x]

        energy_seller_max_quantity[min_seller_index] = energy_seller_max_quantity[min_seller_index] - bought
        buyer_total_requirements[x] = buyer_total_requirements[x] - bought
        key = 'buyer{0}'.format(x)
        if key in allocation_result:
            allocation_result[key]['seller{0}'.format(min_seller_index)] = {
                "price": price_to_be_paid[min_seller_index],
                "quantity": bought
            }
        else:
            allocation_result[key] = {}
            allocation_result[key]['seller{0}'.format(min_seller_index)] = {
                "price": price_to_be_paid[min_seller_index],
                "quantity": bought
            }
        price_to_be_paid[min_seller_index] = 1000
        if sum(energy_seller_max_quantity) == 0:
            flag = 1
            break
    if flag == 1:
        print(allocation_result)
        print("No more saleable energy left")
        sys.exit(0)

print("\n\n\nFinal Allocation Results: ")
pretty_print(allocation_result)
