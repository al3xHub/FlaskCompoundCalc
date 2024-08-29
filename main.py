initial_deposit = 1000
interest = 0.05
contribution = 100
compounding_type = 'monthly'
period_years = 10

if compounding_type == 'monthly':
    n = 12
elif compounding_type == 'quarterly':
    n = 4
else:
    n=1

total_amount = initial_deposit * (1 + interest / n) ** (n * period_years)
total_contributions = contribution * (((1+ interest/n) ** (n * period_years)-1) / (interest /n))

final_amount = total_amount + total_contributions

print(f"Total amount at the end of {period_years} years: ${final_amount:.2f}")