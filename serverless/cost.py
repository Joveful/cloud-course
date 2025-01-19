import numpy as np

# Trying to calculate hits per month; more specifically the convergence
# Long running service cost
# Cost per hour = 0.1 + 0.4 * 0.07377
cph1 = 0.1 + 4 * 0.07377
cost = cph1 * 24 * 30

# Stateless function

cpr = 0.4e-6
cpe = 2.9e-5

nr = (cost + 2e6 * cpr + 4e5 * cpe) / (cpr + cpe * 0.4)
cost2 = nr * cpr + nr * cpe * 0.4
print("Cost of service:", round(cost, 2))
print("cost of serverless:", round(cost2, 2))
print("n_r", round(nr / 1e6, 2))
