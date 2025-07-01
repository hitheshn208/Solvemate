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
    # Extract input values
    func_str = input_data.function
    x0 = input_data.initial_guess
    x_val = input_data.value
    order = input_data.order

    x = sp.symbols('x')
    f = sp.sympify(func_str)

    taylor_sum = 0
    taylor_expansion = []

    for n in range(order + 1):
        # Derivative and its value at x0
        derivative = f.diff(x, n)
        derivative_at_x0 = derivative.subs(x, x0).evalf(4)  # ✅ Round to 4 digits

        # Add term to final approximation
        term = (derivative_at_x0 * (x - x0)**n) / sp.factorial(n)
        taylor_sum += term

        # ✅ Skip 0 terms
        if derivative_at_x0 == 0:
            continue

        # ✅ Handle sign nicely
        sign = "-" if derivative_at_x0 < 0 else "+"
        abs_val = abs(derivative_at_x0)

        # ✅ Avoid leading '+' for the first term
        if not taylor_expansion:
            latex_term = f"{sp.latex(abs_val)} \\frac{{(x - {x0})^{{{n}}}}}{{{sp.factorial(n)}}}"
        else:
            latex_term = f"{sign} {sp.latex(abs_val)} \\frac{{(x - {x0})^{{{n}}}}}{{{sp.factorial(n)}}}"

        taylor_expansion.append(latex_term)

    # Join all terms with spaces for rendering
    taylor_series_str = " ".join(taylor_expansion)

    return {
        "taylor_approximation": round(float(taylor_sum.subs(x, x_val)), 4),  # ✅ Round final answer
        "taylor_series": taylor_series_str  # ✅ Clean LaTeX string
    }
