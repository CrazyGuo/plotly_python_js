from datetime import datetime, date

current_date = date.today()
begin = True
end = date.max

params = {"name": "Alex", "sex":"M", "age":20 }

def test_params(*args, **kwargs):
    print(args)
    print(kwargs)

test_params(**params)

def test_param_name(name, sex, **kwargs):
    print(kwargs)

test_param_name(**params)

if current_date >= begin and current_date <= end:
    print("OK")
    print(current_date)
    print(begin)