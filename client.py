"""
In-Process Isolated Python Namespace REPL Engine.
Zero external dependencies, standard library only.
"""

import sys
import io
import time
import contextlib
from typing import Dict, Any, Optional

SAFE_BUILTINS = {
    "abs": abs, "all": all, "any": any, "bin": bin, "bool": bool,
    "chr": chr, "dict": dict, "dir": dir, "divmod": divmod, "enumerate": enumerate,
    "filter": filter, "float": float, "format": format, "hex": hex, "int": int,
    "isinstance": isinstance, "issubclass": issubclass, "iter": iter, "len": len,
    "list": list, "map": map, "max": max, "min": min, "next": next, "oct": oct,
    "ord": ord, "pow": pow, "print": print, "range": range, "repr": repr,
    "reversed": reversed, "round": round, "set": set, "slice": slice, "sorted": sorted,
    "str": str, "sum": sum, "tuple": tuple, "type": type, "zip": zip
}

class IsolatedNamespaceREPLClient:
    """
    Executes Python scripts within a fresh or stateful isolated namespace:
    - Restricts accessible builtins to safe operations
    - Captures stdout and stderr streams cleanly
    - Preserves execution variables across consecutive turns
    """

    def __init__(self, stateful: bool = True):
        self.stateful = stateful
        self.namespace = {"__builtins__": dict(SAFE_BUILTINS)}

    def execute_code(self, code_str: str) -> Dict[str, Any]:
        """Executes code in isolated namespace and captures runtime output."""
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        start_time = time.time()
        status = "SUCCESS"
        error_msg = None
        eval_result = None

        exec_env = self.namespace if self.stateful else {"__builtins__": dict(SAFE_BUILTINS)}

        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            try:
                # Try evaluating as single expression first
                try:
                    expr_ast = compile(code_str.strip(), "<repl>", "eval")
                    eval_result = eval(expr_ast, exec_env)
                except SyntaxError:
                    # Execute as multi-line statements
                    stmt_ast = compile(code_str, "<repl>", "exec")
                    exec(stmt_ast, exec_env)
            except Exception as e:
                status = "ERROR"
                error_msg = f"{type(e).__name__}: {str(e)}"

        elapsed = round(time.time() - start_time, 4)
        stdout_str = stdout_buf.getvalue()
        stderr_str = stderr_buf.getvalue()

        # Variable keys created (excluding builtins)
        exported_vars = {k: str(v)[:80] for k, v in exec_env.items() if not k.startswith("__")}

        return {
            "status": status,
            "stdout": stdout_str,
            "stderr": stderr_str,
            "eval_result": eval_result,
            "error": error_msg,
            "elapsed_sec": elapsed,
            "active_variables": exported_vars
        }
