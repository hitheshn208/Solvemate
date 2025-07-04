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
    func_str = input_data.function
    x0 = input_data.initial_guess
    x_val = input_data.value
    order = input_data.order

    x = sp.symbols('x')
    f = sp.sympify(func_str)

    try:
        # Generate the full Taylor series
        full_series = f.series(x, x0, order + 1).removeO()
        latex_series = sp.latex(full_series)
        math_expr_str = str(full_series.expand())

        # Generate up to 5 Taylor series of order 1 to 5
        taylor_functions = []
        for n in range(1, min(6, order + 1)):
            approx = f.series(x, x0, n + 1).removeO()
            taylor_functions.append(str(approx.expand()))

        approximation = float(full_series.subs(x, x_val).evalf())

        return {
            "taylor_approximation": round(approximation, 5),
            "taylor_series": latex_series,
            "taylor_expression": math_expr_str,
            "taylor_list": taylor_functions
        }

    except Exception as e:
        return {"error": "Failed to generate Taylor series. Check the input."}
