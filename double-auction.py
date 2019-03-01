"""
This is an implementation of an iterative double auction method with
optimization equations solved using KKT conditions as proposed in
the paper 'Enabling Localized Peer-to-Peer Electricity Trading Among Plug-in
 Hybrid Electric Vehicles Using Consortium Blockchains' published in
 IEEE Transactions.
"""

# Global data variables. Will be initialized to proper values later on
import random

STO = []  # initial states of charging vehicle
C_n = []  # charging vehicle charge exchange
D_n = []  # discharging vehicle charge exchange
B_n = []  # buying bids
S_n = []  # selling bids

eps = 0.01  # converging factor
eta = 0.8  # average charging efficiency
tau = 0.003  # weight-sto relation constant
l1 = 0.01
l2 = 0.015
c_in_max = [18, 15, 17, 14]
c_in_min = [7, 5, 8, 10]
d_in_max = [15, 13, 20, 17, 20]
reward_j_min = [1.1, 1.5, 1.4, 1.9, 1.8]
i = 4
j = 5


# Let us do the experiment with 4 CVs and 5 DVs


def get_j_sum_b_array(t):
    return sum(B_n[t])


def get_rdb(b_t_plus_1, b_t):
    return (b_t_plus_1 - b_t) / b_t


def get_rds(s_t_plus_1, s_t):
    return (s_t_plus_1 - s_t) / s_t


def calculate_next_round_d_values():
    for x in range(0, len(D_n)):
        for y in range(0, len(D_n[0])):
            D_n[x][y] = (S_n[x][y] - l2) / l1


def calculate_next_round_c_values():
    for x in range(0, len(C_n)):
        K3 = get_j_sum_b_array(x)
        K2 = eta * tau / STO[x]
        K = (c_in_min[x] - 1) * K3 / (eta * K3 - K2)
        tmp = (eta * K - c_in_min[x] + 1) / K2
        print(tmp)
        for y in range(0, len(C_n[0])):
            C_n[x][y] = B_n[x][y] * tmp


# Generating random initial charges
for x in range(0, i):
    STO.append(1)
    temp = []
    temp1 = []
    for y in range(0, j):
        temp.append(0.0)
        temp1.append(random.randint(2, 5))
    C_n.append(temp)
    B_n.append(temp1)

print(STO)

for x in range(0, j):
    temp1 = []
    temp = []
    for y in range(0, i):
        temp.append(0.0)
        temp1.append(random.randint(3, 6))
    S_n.append(temp1)
    D_n.append(temp)

flag = 1
print('-----------------------')
print(C_n)
print('-----------------------')
print(D_n)
print('-----------------------')
print(B_n)
print('-----------------------')
print(S_n)
print('-----------------------')

while flag == 1:
    calculate_next_round_d_values()
    calculate_next_round_c_values()
    print(C_n)
    print("==========================")
    print(D_n)
    break

# Not yet complete
