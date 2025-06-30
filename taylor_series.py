from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

class TaylorInput(BaseModel):
    function: str
    initial_guess: float
    value: float
    order: int

@router.post("/taylor")
def taylor_series(input_data: TaylorInput):
    # Extract input data
    func_str = input_data.function
    x0 = input_data.initial_guess
    x_val = input_data.value
    order = input_data.order

    # Setup symbolic variable
    x = sp.symbols('x')
    f = sp.sympify(func_str)

    taylor_sum = 0
    taylor_expansion = []

    # Taylor Series Expansion formula
    for n in range(order + 1):
        derivative = f.diff(x, n)  # n-th derivative
        derivative_at_x0 = derivative.subs(x, x0)
        term = (derivative_at_x0 * (x - x0)**n) / sp.factorial(n)
        taylor_sum += term
        taylor_expansion.append(f"({derivative_at_x0}) * (x - {x0})^{n} / {sp.factorial(n)}")

    # Create the Taylor series string
    taylor_series_str = " + ".join(taylor_expansion)

    return {
        "taylor_approximation": float(taylor_sum.subs(x, x_val)),
        "taylor_series": taylor_series_str
    }
