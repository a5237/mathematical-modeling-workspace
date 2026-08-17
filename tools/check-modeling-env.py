from __future__ import annotations

import importlib
import os
import platform
import shutil
import struct
import subprocess
import sys
from importlib import metadata
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = WORKSPACE_ROOT / "var" / "tmp"
(CACHE_ROOT / "matplotlib").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(CACHE_ROOT / "matplotlib"))


PACKAGES: list[tuple[str, str, bool]] = [
    ("numpy", "numpy", True),
    ("scipy", "scipy", True),
    ("pandas", "pandas", True),
    ("matplotlib", "matplotlib", True),
    ("seaborn", "seaborn", True),
    ("statsmodels", "statsmodels", True),
    ("sklearn", "scikit-learn", True),
    ("pulp", "PuLP", True),
    ("ortools", "ortools", True),
    ("sympy", "sympy", True),
    ("networkx", "networkx", True),
    ("openpyxl", "openpyxl", True),
    ("xlsxwriter", "xlsxwriter", True),
    ("jupyterlab", "jupyterlab", True),
    ("xgboost", "xgboost", True),
    ("lightgbm", "lightgbm", True),
    ("pymoo", "pymoo", True),
    ("deap", "deap", True),
    ("plotly", "plotly", True),
    ("xlrd", "xlrd", True),
    ("jieba", "jieba", True),
    ("wordcloud", "wordcloud", True),
    ("pydot", "pydot", True),
    ("torch", "torch", False),
    ("torchvision", "torchvision", False),
    ("torchaudio", "torchaudio", False),
]


def version_of(distribution: str, module: object) -> str:
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return getattr(module, "__version__", "unknown")


def check_imports() -> bool:
    print("\n[Python packages]")
    ok = True
    for module_name, distribution, required in PACKAGES:
        try:
            module = importlib.import_module(module_name)
            print(f"  OK   {distribution:<18} {version_of(distribution, module)}")
        except Exception as exc:
            label = "MISS" if required else "SKIP"
            print(f"  {label} {distribution:<18} {exc.__class__.__name__}: {exc}")
            if required:
                ok = False
    return ok


def check_graphviz() -> None:
    print("\n[Graphviz]")
    dot_path = shutil.which("dot")
    if not dot_path:
        print("  pydot Python package is installed, but Graphviz 'dot' is not on PATH.")
        print("  Install Graphviz separately and add its bin directory to PATH for rendering.")
        return
    print(f"  dot executable: {dot_path}")
    try:
        result = subprocess.run(
            ["dot", "-V"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        version_text = (result.stderr or result.stdout).strip()
        print(f"  dot version: {version_text}")
    except Exception as exc:
        print(f"  dot exists but version check failed: {exc}")


def run_smoke_tests() -> bool:
    print("\n[Smoke tests]")
    ok = True

    try:
        import numpy as np

        arr = np.array([1.0, 2.0, 3.0])
        assert float(arr.mean()) == 2.0
        print("  OK   NumPy mean")
    except Exception as exc:
        ok = False
        print(f"  FAIL NumPy: {exc}")

    try:
        import pandas as pd

        df = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
        assert int(df["y"].sum()) == 12
        print("  OK   Pandas DataFrame")
    except Exception as exc:
        ok = False
        print(f"  FAIL Pandas: {exc}")

    try:
        from scipy.optimize import minimize

        result = minimize(lambda z: (z[0] - 2.0) ** 2, x0=[0.0])
        assert result.success and abs(result.x[0] - 2.0) < 1e-4
        print("  OK   SciPy optimize")
    except Exception as exc:
        ok = False
        print(f"  FAIL SciPy: {exc}")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_dir = CACHE_ROOT / "environment-check"
        fig_dir.mkdir(parents=True, exist_ok=True)
        fig_path = fig_dir / "modeling_env_smoke.png"
        plt.figure(figsize=(4, 3), dpi=120)
        plt.plot([0, 1, 2], [0, 1, 4], marker="o")
        plt.title("Modeling env smoke test")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        print(f"  OK   Matplotlib saved {fig_path}")
    except Exception as exc:
        ok = False
        print(f"  FAIL Matplotlib: {exc}")

    try:
        from sklearn.linear_model import LinearRegression
        import numpy as np

        x = np.array([[1.0], [2.0], [3.0]])
        y = np.array([2.0, 4.0, 6.0])
        model = LinearRegression().fit(x, y)
        assert abs(float(model.coef_[0]) - 2.0) < 1e-8
        print("  OK   scikit-learn LinearRegression")
    except Exception as exc:
        ok = False
        print(f"  FAIL scikit-learn: {exc}")

    try:
        import pulp

        problem = pulp.LpProblem("smoke", pulp.LpMaximize)
        x = pulp.LpVariable("x", lowBound=0)
        problem += x
        problem += x <= 3
        status = problem.solve(pulp.PULP_CBC_CMD(msg=False))
        assert pulp.LpStatus[status] == "Optimal" and abs(x.value() - 3.0) < 1e-8
        print("  OK   PuLP CBC optimization")
    except Exception as exc:
        ok = False
        print(f"  FAIL PuLP optimization: {exc}")

    try:
        from ortools.linear_solver import pywraplp

        solver = pywraplp.Solver.CreateSolver("GLOP")
        if solver is None:
            raise RuntimeError("GLOP solver is not available")
        y = solver.NumVar(0, solver.infinity(), "y")
        solver.Maximize(y)
        solver.Add(y <= 5)
        status = solver.Solve()
        assert status == pywraplp.Solver.OPTIMAL and abs(y.solution_value() - 5.0) < 1e-8
        print("  OK   OR-Tools linear optimization")
    except Exception as exc:
        ok = False
        print(f"  FAIL OR-Tools optimization: {exc}")

    return ok


def main() -> int:
    print("[Python runtime]")
    print(f"  version:     {sys.version.replace(chr(10), ' ')}")
    print(f"  executable:  {sys.executable}")
    print(f"  platform:    {platform.platform()}")
    print(f"  architecture:{platform.architecture()[0]}")
    print(f"  pointer bits:{struct.calcsize('P') * 8}")
    print(f"  MPLCONFIGDIR:{os.environ['MPLCONFIGDIR']}")

    imports_ok = check_imports()
    check_graphviz()
    tests_ok = run_smoke_tests()

    if imports_ok and tests_ok:
        print("\nRESULT: PASS")
        return 0
    print("\nRESULT: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
