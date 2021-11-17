def defender(func):
    def wrapper(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except ZeroDivisionError:
            return "you can`t use zero as denominator."
        return value

    return wrapper


@defender
def plus(x, y):
    return x / y


print(plus(100, 30))
