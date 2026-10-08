import streamlit as st
import pandas as pd
import joblib

from advisor import create_financial_advice

# Load model and scaler
model = joblib.load("model/financial_advisor_model.pkl")
scaler = joblib.load("model/financial_scaler.pkl")

st.set_page_config(
    page_title="Student Financial Advisor AI",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Student Financial Advisor AI")
st.write(
    "Get an AI-based financial plan for managing your student income."
)

st.divider()

# Student information
st.header("📋 Student Information")

income = st.number_input(
    "Total income received (RWF)",
    min_value=10000,
    max_value=10000000,
    value=80000,
    step=5000
)

months = st.number_input(
    "How many months should this money cover?",
    min_value=1,
    max_value=12,
    value=2
)

lives_alone = st.selectbox(
    "Do you live alone?",
    ["Yes", "No"]
)

school_distance = st.number_input(
    "Distance from your accommodation to school (km)",
    min_value=0.0,
    max_value=50.0,
    value=1.0,
    step=0.5
)

cooks_at_home = st.selectbox(
    "Do you cook at home?",
    ["Yes", "No"]
)

transport_required = st.selectbox(
    "Do you normally need transport to school?",
    ["No", "Yes"]
)

family_support = st.selectbox(
    "Do you receive additional family support?",
    ["No", "Yes"]
)

# Convert answers
alone_value = 1 if lives_alone == "Yes" else 0
cook_value = 1 if cooks_at_home == "Yes" else 0
transport_value = 1 if transport_required == "Yes" else 0
family_value = 1 if family_support == "Yes" else 0


if st.button("🤖 Get My Financial Advice", use_container_width=True):

    # Prepare input
    input_data = pd.DataFrame([{
        "income": income,
        "months": months,
        "lives_alone": alone_value,
        "school_distance_km": school_distance,
        "cooks_at_home": cook_value,
        "transport_required": transport_value,
        "family_support": family_value
    }])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # FNN prediction
    prediction = model.predict(input_scaled)[0]

    # Generate advice
    result = create_financial_advice(
        income=income,
        months=months,
        lives_alone=alone_value,
        school_distance_km=school_distance,
        cooks_at_home=cook_value,
        transport_required=transport_value,
        family_support=family_value,
        plan=prediction
    )

    st.divider()

    # AI recommendation
    st.header("🤖 AI Recommendation")

    if prediction == "survival":
        st.warning("Recommended Plan: SURVIVAL")
    elif prediction == "balanced":
        st.success("Recommended Plan: BALANCED")
    else:
        st.info("Recommended Plan: COMFORTABLE")

    st.write(
        f"The AI recommends a **{prediction}** financial plan "
        f"based on your situation."
    )

    # ==================================================
    # FULL PERIOD BUDGET
    # ==================================================

    st.header(f"💰 Your {months}-Month Financial Plan")

    st.write(
        f"You received **{income:,.0f} RWF** to manage for "
        f"**{months} month(s)**."
    )

    # Convert monthly recommendations to full-period amounts
    rent_total = result["rent"] * months
    food_total = result["food"] * months
    transport_total = result["transport"] * months
    data_total = result["data"] * months
    personal_total = result["personal"] * months
    emergency_total = result["emergency"] * months

    total_period = (
        rent_total
        + food_total
        + transport_total
        + data_total
        + personal_total
        + emergency_total
    )

    remaining = income - total_period

    budget = pd.DataFrame({
        "Category": [
            "🏠 Rent",
            "🍲 Food",
            "🚌 Transport",
            "📱 Data/Airtime",
            "👤 Personal Needs",
            "🚨 Emergency/Savings"
        ],
        "Full Period (RWF)": [
            round(rent_total),
            round(food_total),
            round(transport_total),
            round(data_total),
            round(personal_total),
            round(emergency_total)
        ]
    })

    st.table(budget)

    st.metric(
        "Total Recommended Spending",
        f"{total_period:,.0f} RWF"
    )

    st.metric(
        "Money Remaining",
        f"{remaining:,.0f} RWF"
    )

    # ==================================================
    # MONTHLY VIEW
    # ==================================================

    st.subheader("📅 Monthly Equivalent")

    monthly_budget = pd.DataFrame({
        "Category": [
            "Rent",
            "Food",
            "Transport",
            "Data/Airtime",
            "Personal Needs",
            "Emergency/Savings"
        ],
        "Per Month (RWF)": [
            round(result["rent"]),
            round(result["food"]),
            round(result["transport"]),
            round(result["data"]),
            round(result["personal"]),
            round(result["emergency"])
        ]
    })

    st.table(monthly_budget)

    # ==================================================
    # PRACTICAL ADVICE
    # ==================================================

    st.subheader("📌 What You Should Do")

    for item in result["general_advice"]:
        st.write("✅", item)

    st.write("🚶", result["transport_advice"])
    st.write("🍲", result["food_advice"])

    # ==================================================
    # WARNING
    # ==================================================

    if remaining < 0:

        st.error(
            "⚠️ Your recommended expenses are higher than the "
            "money you received. You should reduce unnecessary expenses."
        )

    elif remaining < 2000:

        st.warning(
            "⚠️ Your remaining money is very small. "
            "Try to reduce unnecessary spending."
        )

    else:

        st.success(
            "✅ Your plan leaves money available for unexpected "
            "expenses or additional savings."
        )

st.divider()

st.caption(
    "Student Financial Advisor AI | Educational budgeting guidance only."
)
