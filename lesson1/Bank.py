def bank(deposit, interest_rate, years):
    if years == 1:
        return deposit * (1.0 + interest_rate / 100)
    else:
        return bank(deposit * (1.0 + interest_rate / 100), interest_rate, years - 1)

print(bank(100,10,4))