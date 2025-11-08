import re
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/operations/add")
def add_nums(a, b):
    return a + b


@app.get("/operations/deduct")
def deduct_nums(a, b):
    return a - b


@app.get("/operations/multiply")
def multiply_nums(a, b):
    return a * b


@app.get("/operations/divide")
def divide_nums(a, b):
    return a * b


@app.get("/operations/all_operations")
def all_operations(a, b, operation):
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return a / b
    else:
        return "Invalid operation"


@app.get("/operations/check")
def check_expression():
    a = input("first number: ")
    print(a)
    operation = input("operation (+, -, *, /): ")
    print(f"{a} {operation} ")
    b = input("second number: ")
    print(f"{a} {operation} {b}")
    input("Press Enter to calculate...")
    result = all_operations(float(a), float(b), operation)
    print(f"{a} {operation} {b} = {result}")


@app.get("/operations/complex")
def complex_calc(expression):
    return eval(expression)

