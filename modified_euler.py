from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

# Input model for Modified Euler
class ModifiedEulerInput(BaseModel):
    function: str
    x0: float
    y0: float
    x_target: float
    h: float

@router.post("/modified_euler")
def modified_euler_method(data: ModifiedEulerInput):
    x, y = sp.symbols('x y')

    try:
        f_expr = sp.sympify(data.function)
        f_lambda = sp.lambdify((x, y), f_expr, modules=["math"])
    except Exception:
        return {"error": "❌ Invalid function."}

    x_val = data.x0
    y_val = data.y0
    h = data.h
    steps = []

    while x_val <= data.x_target + 1e-8:
        try:
            f1 = f_lambda(x_val, y_val)  # slope at (x_n, y_n)
            y_predict = y_val + h * f1   # Euler prediction
            f2 = f_lambda(x_val + h, y_predict)  # slope at (x_{n+1}, y_predict)
            y_final = y_val + (h / 2) * (f1 + f2)  # corrected y

            steps.append({
                "step": len(steps),
                "x": round(x_val, 4),
                "y_n": round(y_val, 4),
                "y_predict": round(y_predict, 4),
                "f1": round(f1, 4),
                "f2": round(f2, 4),
                "y_final": round(y_final, 4)
            })

            x_val = round(x_val + h, 10)  # advance x
            y_val = y_final               # update y

        except Exception:
            return {"error": f"❌ Could not evaluate at x = {x_val}, y = {y_val}"}

    return {
        "result": round(y_val, 4),
        "steps": steps
    }

