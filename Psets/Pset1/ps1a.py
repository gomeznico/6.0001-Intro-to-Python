# Part A: house Hunting

portion_down_payment = 0.25
current_savings = 0.0
r = 0.04 # annual rate of return

annual_salary = float(input('What is your annual salary? : ' ))
monthly_salary = annual_salary/12
portion_saved = float(input("How much of your salary will you save, as a decimal? : "))
total_cost = float(input("What is the price of your home? :"))

### Test case 1
# annual_salary = 120000
# monthly_salary = annual_salary/12
# portion_saved = 0.10
# total_cost = 1000000


### Test case 2
# annual_salary = 80000
# monthly_salary = annual_salary/12
# portion_saved = 0.15
# total_cost = 500000

down_payment = portion_down_payment*total_cost
months = 0

while current_savings < down_payment:
  months += 1
  current_savings += current_savings*r/12
  current_savings += monthly_salary*portion_saved

print('Number of months: ', months )


