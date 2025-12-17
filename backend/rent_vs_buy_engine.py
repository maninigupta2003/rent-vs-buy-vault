# Deterministic rent vs buy calculations
def rent_vs_buy_analysis(
    monthly_income: float,
    annual_rent: float,
    years: int = 5
):
    rent_burn = annual_rent * years

    estimated_affordable_price = monthly_income * 60  # conservative multiplier

    return {
        "annual_rent": annual_rent,
        "years": years,
        "total_rent_paid": rent_burn,
        "affordable_property_estimate": estimated_affordable_price,
        "narrative_anchor": (
            f"You are spending {rent_burn:,.0f} AED on rent over {years} years. "
            "That money builds zero equity."
        )
    }
