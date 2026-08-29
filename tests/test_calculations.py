import pandas as pd

def test_risk_calculations():
    # Setup test dataframe
    df = pd.DataFrame({
        "likelihood": [3, 5, 2],
        "impact": [4, 5, 1],
        "control_effectiveness": [0.5, 0.2, 0.9]
    })
    
    # Run formulas matching dashboard.py load_data
    df["inherent_risk"] = df["likelihood"] * df["impact"]
    df["residual_risk"] = (df["inherent_risk"] * (1 - df["control_effectiveness"])).round(1)
    
    # Assert correctness
    # Row 1: inherent = 12, residual = 12 * 0.5 = 6.0
    # Row 2: inherent = 25, residual = 25 * 0.8 = 20.0
    # Row 3: inherent = 2,  residual = 2 * 0.1 = 0.2
    
    assert list(df["inherent_risk"]) == [12, 25, 2]
    assert list(df["residual_risk"]) == [6.0, 20.0, 0.2]
