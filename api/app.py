from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# --- Simplified bracket model (DEMO ONLY) ---
# Single filer 2024-ish rough demo (NOT exact/official).
BRACKETS_SINGLE = [
    (0,       11600,  0.10),
    (11600,   47150,  0.12),
    (47150,  100525,  0.22),
    (100525, 191950,  0.24),
]
STANDARD_DEDUCTION = {
    "single": 14600,
    "married_joint": 29200,
}

def estimate_tax(income: float, filing_status: str = "single"):
    # very simplified: taxable = max(0, income - standard deduction)
    deduction = STANDARD_DEDUCTION.get(filing_status, STANDARD_DEDUCTION["single"])
    taxable = max(0.0, income - deduction)
    tax = 0.0
    # piecewise calc
    for lo, hi, rate in BRACKETS_SINGLE:
        if taxable > lo:
            portion = min(taxable, hi) - lo
            if portion > 0:
                tax += portion * rate
    return round(tax, 2), round(taxable, 2)

@app.route("/estimate", methods=["POST"])
def estimate():
    """
    Request JSON:
    {
      "filing_status": "single" | "married_joint",
      "wages": 68000,
      "withheld_federal": 7200
    }
    """
    data = request.get_json(force=True)
    filing_status = data.get("filing_status", "single")
    wages = float(data.get("wages", 0))
    withheld = float(data.get("withheld_federal", 0))
    est_tax, taxable = estimate_tax(wages, filing_status)
    refund_or_due = round(withheld - est_tax, 2)
    return jsonify({
        "filing_status": filing_status,
        "wages": wages,
        "taxable_income": taxable,
        "estimated_tax": est_tax,
        "withheld_federal": withheld,
        "refund_or_amount_due": refund_or_due
    })

@app.route("/w2", methods=["GET"])
def w2():
    """Returns sample W-2-like data from CSV."""
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_w2.csv")
    df = pd.read_csv(csv_path)
    return df.to_json(orient="records")

@app.route("/")
def health():
    return jsonify({"service": "tax-filing-demo", "status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
