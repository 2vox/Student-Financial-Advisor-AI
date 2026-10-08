def create_financial_advice(
    income,
    months,
    lives_alone,
    school_distance_km,
    cooks_at_home,
    transport_required,
    family_support,
    plan
):
    monthly_income = income / months

    # Recommended rent
    if monthly_income <= 40000:
        rent = 15000
    elif monthly_income <= 60000:
        rent = 20000
    else:
        rent = min(30000, monthly_income * 0.30)

    # Transport
    if school_distance_km <= 2 and transport_required == 0:
        transport = 0
        transport_advice = "Walk to school when safe. Avoid unnecessary transport costs."
    elif transport_required == 1:
        transport = monthly_income * 0.10
        transport_advice = "Use transport only when necessary and choose the cheapest reliable option."
    else:
        transport = 0
        transport_advice = "Try to choose accommodation close to school."

    # Food
    if cooks_at_home == 1:
        food = monthly_income * 0.30
        food_advice = "Cook at home and buy basic food in bulk to reduce costs."
    else:
        food = monthly_income * 0.40
        food_advice = "Cooking at home is strongly recommended to reduce food expenses."

    # Data / airtime
    data = monthly_income * 0.08

    # Personal needs
    personal = monthly_income * 0.07

    # Emergency/savings
    emergency = monthly_income * 0.15

    # Total recommended monthly budget
    total = rent + transport + food + data + personal + emergency

    # Adjust emergency if budget is too high
    if total > monthly_income:
        emergency = max(0, monthly_income - (
            rent + transport + food + data + personal
        ))
        total = rent + transport + food + data + personal + emergency

    # Advice
    advice = []

    if plan == "survival":
        advice.append("Your income is limited. Focus only on essential needs.")
        advice.append("Choose low-cost accommodation close to school.")
        advice.append("Avoid unnecessary transport and entertainment.")

    elif plan == "balanced":
        advice.append("Use a simple monthly budget and control unnecessary spending.")
        advice.append("Keep part of your money as an emergency reserve.")
        advice.append("Plan your food for the whole period instead of spending daily.")

    elif plan == "comfortable":
        advice.append("Your income gives you more flexibility, but you should still save.")
        advice.append("Avoid increasing your lifestyle unnecessarily.")
        advice.append("Keep an emergency fund for unexpected student expenses.")

    if lives_alone == 1:
        advice.append("Because you live alone, prioritize affordable rent and food planning.")

    if school_distance_km <= 2:
        advice.append("Your school is close, so walking can save significant transport money.")

    if family_support == 1:
        advice.append("Use family support for important needs and continue building your own savings.")

    if cooks_at_home == 1:
        advice.append("Continue cooking at home and consider buying food supplies in bulk.")

    return {
        "monthly_income": monthly_income,
        "rent": rent,
        "transport": transport,
        "food": food,
        "data": data,
        "personal": personal,
        "emergency": emergency,
        "total": total,
        "transport_advice": transport_advice,
        "food_advice": food_advice,
        "general_advice": advice
    }