from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

class NR2Input(BaseModel):
    f1: str
    f2: str
    x0: float
    y0: float
    tolerance: float = 1e-5
    max_iterations: int = 20

@router.post("/newton_raphson_2_var")
def newton_raphson_2var(data: NR2Input):
    x, y = sp.symbols('x y')
    f1 = sp.sympify(data.f1)
    f2 = sp.sympify(data.f2)

    x0 = data.x0
    y0 = data.y0

    jacobian = sp.Matrix([
        [sp.diff(f1, x), sp.diff(f1, y)],
        [sp.diff(f2, x), sp.diff(f2, y)]
    ])

    F = sp.Matrix([f1, f2])
    iterations = []

    for i in range(data.max_iterations):
        J_sub = jacobian.subs({x: x0, y: y0}).evalf()
        F_sub = F.subs({x: x0, y: y0}).evalf()

        try:
            delta = J_sub.inv() * (-F_sub)
        except:
            return {"error": "Jacobian is singular or non-invertible."}

        x1 = x0 + delta[0]
        y1 = y0 + delta[1]
        error = max(abs(x1 - x0), abs(y1 - y0))

        iterations.append({
            "iteration": i + 1,
            "x": round(float(x0), 5),
            "y": round(float(y0), 5),
            "f1": round(float(F_sub[0]), 5),
            "f2": round(float(F_sub[1]), 5),
            "next_x": round(float(x1), 5),
            "next_y": round(float(y1), 5),
            "error": round(float(error), 5)
        })

        if error < data.tolerance:
            break

        x0, y0 = x1, y1

    return {
        "root": [round(float(x1), 5), round(float(y1), 5)],
        "iterations": iterations
    }
