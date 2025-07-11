from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import sympy as sp

router = APIRouter()

class RK4Input(BaseModel):
    function: str
    x0: str
    y0: str
    h: float
    xn: float

@router.post("/rk4")
def runge_kutta(data: RK4Input):
    x, y = sp.symbols('x y')
    try:
        f = sp.sympify(data.function)
        fx = sp.lambdify((x, y), f)

        x0 = float(sp.sympify(data.x0))
        y0 = float(sp.sympify(data.y0))
        h = float(data.h)
        xn = float(data.xn)

        steps = []
        n = int((xn - x0) / h)

        for i in range(n + 1):
            k1 = h * fx(x0, y0)
            k2 = h * fx(x0 + h / 2, y0 + k1 / 2)
            k3 = h * fx(x0 + h / 2, y0 + k2 / 2)
            k4 = h * fx(x0 + h, y0 + k3)

            yn1 = y0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6

            steps.append({
                "step": i,
                "x": round(x0, 4),
                "y": round(y0, 4),
                "k1": round(k1, 4),
                "k2": round(k2, 4),
                "k3": round(k3, 4),
                "k4": round(k4, 4),
                "yn1": round(yn1, 4)
            })

            x0 += h
            y0 = yn1

        return {"steps": steps,
        "final_y": steps[-1]["yn1"] } 
    
    except Exception as e:
        return JSONResponse(status_code=422, content={"error": "Invalid input. Use correct function and numeric values."})
