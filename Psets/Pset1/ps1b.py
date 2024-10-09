# Part B: Saving with a raise

portion_down_payment = 0.25
current_savings = 0.0
r = 0.04 # annual rate of return

annual_salary = float(input("Enter your starting annual salary: " ))
monthly_salary = annual_salary/12
portion_saved = float(input("Enter the percent of your salary to save as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semiannual raise, as a decimal"))

### Test case 1
# annual_salary = 120000
# monthly_salary = annual_salary/12
# portion_saved = 0.10
# total_cost = 500000
# semi_annual_raise = .03


### Test case 2
# annual_salary = 80000
# monthly_salary = annual_salary/12
# portion_saved = 0.1
# total_cost = 800000
# semi_annual_raise = .03

### Test case 3
# annual_salary = 75000
# monthly_salary = annual_salary/12
# portion_saved = 0.05
# total_cost = 1500000
# semi_annual_raise = .05


down_payment = portion_down_payment*total_cost
months = 0

while current_savings < down_payment:
  months += 1
  current_savings += current_savings*r/12
  current_savings += monthly_salary*portion_saved
  if (months%6 == 0):
    monthly_salary+= monthly_salary*semi_annual_raise

print('Number of months: ', months )
