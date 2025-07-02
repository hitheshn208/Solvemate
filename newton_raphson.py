from fastapi import APIRouter
from pydantic import BaseModel
import sympy as sp

router = APIRouter()

class NRInput(BaseModel):
    function: str
    initial_guess: float
    tolerance: float = 1e-5
    max_iterations: int = 20

@router.post("/newton")
def newton_raphson(data: NRInput):
    x = sp.symbols('x')
    f = sp.sympify(data.function)
    f_prime = sp.diff(f, x)

    xi = data.initial_guess
    tolerance = data.tolerance
    max_iter = data.max_iterations

    iterations = []

    for i in range(max_iter):
        f_val = f.subs(x, xi).evalf()
        f_prime_val = f_prime.subs(x, xi).evalf()

        if f_prime_val == 0:
            return {"error": "Derivative is zero. Stopping."}

        xi_new = xi - f_val / f_prime_val
        error = abs(xi_new - xi)

        iterations.append({
            "iteration": i + 1,
            "x": round(float(xi), 5),
            "f(x)": round(float(f_val), 5),
            "f'(x)": round(float(f_prime_val), 5),
            "next_x": round(float(xi_new), 5),
            "error": round(float(error), 5)
        })

        if error < tolerance:
            break

        xi = xi_new

    return {
        "root": round(float(xi_new), 5),
        "iterations": iterations
    }
