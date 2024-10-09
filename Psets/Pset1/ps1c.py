# Part C: Finding out the right amount to save away


# assumptions
semi_annual_raise = .07
portion_down_payment = 0.25
current_savings = 0.0
r = 0.04 # annual rate of return
total_cost = 1000000.0 #1 million

annual_salary = float(input("Enter your starting annual salary: " ))
monthly_salary = annual_salary/12

### Test case 1
# annual_salary = 150000
# monthly_salary = annual_salary/12

### Test case 2
# annual_salary = 300000
# monthly_salary = annual_salary/12

### Test case 3
# annual_salary = 10000
# monthly_salary = annual_salary/12

def totalSaved(portion_saved, monthly_income):
  savings = 0
  for months in range(1,37):
    savings += savings*r/12
    savings += (monthly_income*portion_saved)/10_000
    if (months%6 == 0):
      monthly_income+= monthly_income*semi_annual_raise
  return savings

down_payment = portion_down_payment*total_cost
high = 10_000
low = 0
guessed_portion_saved = int((high+low)/2)
steps = 0
diff = down_payment - current_savings

## test if possible with 100% savings
savings = totalSaved(10_000, monthly_salary)
if savings < down_payment:
  print("It is not possible to pay the down payment in three years.")
  quit()



while (diff < -100) or (diff > 100):
  steps +=1
  savings = totalSaved(guessed_portion_saved, monthly_salary)
  diff = savings - down_payment
  if diff < -100:
    # if diff is negative, need to save more, increase savings rate
    low = guessed_portion_saved
    guessed_portion_saved = int((high + low)/2)
  elif diff > 100:
    # if diff is positive, saved too much, lower savings rate
    high = guessed_portion_saved
    guessed_portion_saved = int((high + low)/2)
  else:
    print ("Best Savings rate: ", guessed_portion_saved/10_000)
    print ("Steps in bisestion search: ", steps)
    break
  if steps > 30:
    print('taking too long')
    quit()
