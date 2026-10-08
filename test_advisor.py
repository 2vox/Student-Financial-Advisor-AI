from advisor import create_financial_advice

result = create_financial_advice(
    income=80000,
    months=2,
    lives_alone=1,
    school_distance_km=1,
    cooks_at_home=1,
    transport_required=0,
    family_support=0,
    plan="balanced"
)

print("===== STUDENT FINANCIAL ADVICE =====")
print(f"Monthly income: {result['monthly_income']:.0f} RWF")
print(f"Rent: {result['rent']:.0f} RWF")
print(f"Transport: {result['transport']:.0f} RWF")
print(f"Food: {result['food']:.0f} RWF")
print(f"Data/Airtime: {result['data']:.0f} RWF")
print(f"Personal: {result['personal']:.0f} RWF")
print(f"Emergency: {result['emergency']:.0f} RWF")
print(f"Total: {result['total']:.0f} RWF")

print("\nAdvice:")
for item in result["general_advice"]:
    print("-", item)

print("\n" + result["transport_advice"])
print(result["food_advice"])