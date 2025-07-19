from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

class EulerInput(BaseModel):
    function: str   
    x0: float       # Initial x
    y0: float       # Initial y(x0)
    x_target: float # Final x value
    h: float        # Step size

@router.post("/euler")
def euler_method(data: EulerInput):
    x, y = sp.symbols('x y')

    try:
        f_expr = sp.sympify(data.function)  # user enters dy/dx = f(x, y)
        f_lambda = sp.lambdify((x, y), f_expr, modules=["math"])
    except Exception:
        return {"error": "Invalid function format."}

    x_val = data.x0
    y_val = data.y0
    h = data.h
    target = data.x_target
    steps = []

    while x_val <= target + 1e-8:
        steps.append({
            "x": round(x_val, 4),
            "y": round(y_val, 4)
        })
        try:
            y_val += h * f_lambda(x_val, y_val)
        except Exception:
            return {"error": f"❌ Could not evaluate f(x, y) at x = {x_val}, y = {y_val}"}
        x_val = round(x_val + h, 10)

    return {
        "result": round(y_val, 4),
        "steps": steps
    }
