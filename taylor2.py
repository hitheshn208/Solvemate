from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

class Taylor2Input(BaseModel):
    function: str
    x0: str
    y0: str
    order: int

@router.post("/taylor2")
def taylor_series_two_var(data: Taylor2Input):
    x, y = sp.symbols('x y')
    
    try:
        f = sp.sympify(data.function)
        x0 = float(sp.sympify(data.x0))
        y0 = float(sp.sympify(data.y0))
    except Exception:
        return {"error": "❌ Invalid input for x0 or y0. Please use numeric values like 1, pi, sqrt(2)."}
    
    order = min(data.order, 4)  # limit to 4

    taylor = 0
    terms = []

    for i in range(order + 1):
        for j in range(order + 1 - i):
            deriv = f.diff(x, i).diff(y, j)
            coeff = deriv.subs({x: x0, y: y0}) / (sp.factorial(i) * sp.factorial(j))
            term = coeff * (x - x0)**i * (y - y0)**j
            taylor += term
            if coeff != 0:
                terms.append(term)

    latex = sp.latex(taylor.simplify())
    expr = str(taylor.expand())

    return {
        "latex": latex,
        "expression": expr
    }
