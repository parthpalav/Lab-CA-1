def calculate(expression):
    try:
        return eval(expression)
    except:
        return "Error in calculation"