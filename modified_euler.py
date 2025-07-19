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

    while round(x_val, 10) < round(data.x_target, 10):  # ✅ avoid overshooting
        try:
            f1 = f_lambda(x_val, y_val)
            y_predict = y_val + h * f1

            f2 = f_lambda(x_val + h, y_predict)
            y_corr = y_val + (h / 2) * (f1 + f2)

            f3 = f_lambda(x_val + h, y_corr)
            y_final = y_val + (h / 2) * (f1 + f3)

            steps.append({
                "step": len(steps),
                "x": round(x_val, 4),
                "y_n": round(y_val, 4),
                "y_predict": round(y_predict, 4),
                "f1": round(f1, 4),
                "f2": round(f2, 4),
                "f3": round(f3, 4),
                "y_final": round(y_final, 4),
                "evaluations": 3
            })

            x_val = x_val + h
            y_val = y_final  # ✅ update using full precision

        except Exception:
            return {"error": f"❌ Could not evaluate at x = {x_val}, y = {y_val}"}

    return {
        "result": round(y_val, 4),   # ✅ Final result to 4 decimals
        "steps": steps
    }
