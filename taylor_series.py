from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

class TaylorInput(BaseModel):
    function: str
    initial_guess: str
    value: str
    order: int

@router.post("/taylor")
def taylor_series(input_data: TaylorInput):
    try:
        func_str = input_data.function
        x0 = sp.sympify(input_data.initial_guess)  
        x_val = sp.sympify(input_data.value)        
    except Exception:
        return {
            "error": "Invalid input for initial guess or value. Use numbers like pi/2 or sqrt(2)."
        }

    order = input_data.order
    x = sp.symbols('x')

    try:
        # ✅ Let sympify recognize functions like sin, cos, etc.
        f = sp.sympify(func_str, locals=sp.__dict__)

        # Generate the full Taylor series at x0
        full_series = f.series(x, x0, order + 1).removeO()
        latex_series = sp.latex(full_series)
        math_expr_str = str(full_series.expand())

        # Generate up to 5 Taylor series of increasing order
        taylor_functions = []
        for n in range(1, min(6, order + 1)):
            approx = f.series(x, x0, n + 1).removeO()
            taylor_functions.append(str(approx.expand()))

        # Evaluate the final full series at x_val
        approximation = float(full_series.subs(x, x_val).evalf())

        return {
            "taylor_approximation": round(approximation, 5),
            "taylor_series": latex_series,
            "taylor_expression": math_expr_str,
            "taylor_list": taylor_functions
        }

    except Exception as e:
        return {"error": f"Failed to generate Taylor series. Check the input.\n{str(e)}"}
