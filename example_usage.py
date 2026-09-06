"""
Demonstration of genpark-inprocess-python-repl-isolated-namespace-skill
"""

from client import IsolatedNamespaceREPLClient

def main():
    repl = IsolatedNamespaceREPLClient(stateful=True)

    # Step 1: Define variables and functions
    step1 = repl.execute_code("""
prices = [19.99, 45.50, 120.00, 5.25]
tax_rate = 0.08
total_with_tax = sum(prices) * (1 + tax_rate)
print(f"Total calculated: ${total_with_tax:.2f}")
""")
    print("=== STEP 1 EXECUTION ===")
    print("Stdout:", step1["stdout"].strip())
    print("Variables:", step1["active_variables"])

    # Step 2: Query result in stateful session
    step2 = repl.execute_code("round(total_with_tax, 2)")
    print("\n=== STEP 2 EVALUATION ===")
    print("Eval Result:", step2["eval_result"])
    print("Status:", step2["status"])

if __name__ == "__main__":
    main()
