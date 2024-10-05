import streamlit as st

# Federal tax brackets for single filers (2024)
federal_brackets = [
    (11000, 0.10),
    (44725, 0.12),
    (95375, 0.22),
    (182100, 0.24),
    (231250, 0.32),
    (578125, 0.35),
    (float('inf'), 0.37)  # highest tax bracket
]

# New York State tax brackets for single filers (2024)
ny_state_brackets = [
    (8500, 0.04),
    (11700, 0.045),
    (13900, 0.0525),
    (21400, 0.059),
    (80650, 0.0633),
    (215400, 0.0685),
    (1077550, 0.0965),
    (float('inf'), 0.103)
]

# NYC tax brackets for single filers (2024)
nyc_brackets = [
    (12000, 0.03078),
    (25000, 0.03762),
    (50000, 0.03819),
    (float('inf'), 0.03876)
]

# California State tax brackets for single filers (2024)
ca_state_brackets = [
    (10099, 0.01),
    (23942, 0.02),
    (37788, 0.04),
    (52455, 0.06),
    (66295, 0.08),
    (338639, 0.093),
    (406364, 0.103),
    (677275, 0.113),
    (float('inf'), 0.123)
]

# Function to calculate progressive taxes
def calculate_tax(income, brackets):
    tax = 0
    previous_limit = 0
    for limit, rate in brackets:
        if income > limit:
            tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate
            break
    return tax

# Function to calculate net income after taxes
def calculate_net_income(ctc, state, city):
    # Calculate federal tax
    federal_tax = calculate_tax(ctc, federal_brackets)
    
    # Calculate state and city taxes based on user selection
    if state == "New York" and city == "New York City":
        state_tax = calculate_tax(ctc, ny_state_brackets)
        city_tax = calculate_tax(ctc, nyc_brackets)
    elif state == "California" and city == "Bay Area":
        state_tax = calculate_tax(ctc, ca_state_brackets)
        city_tax = 0  # No city-specific tax for Bay Area
    else:
        state_tax = 0
        city_tax = 0
    
    total_tax = federal_tax + state_tax + city_tax

    # Calculate net income after taxes
    net_annual_income = ctc - total_tax
    net_monthly_income = net_annual_income / 12
    net_weekly_income = net_annual_income / 52
    net_hourly_income = net_weekly_income / 40  # Assuming 40-hour workweeks

    # Gross hourly rate for comparison
    gross_hourly_rate = (ctc / 52) / 40  # Initial hourly rate based on gross income

    # Hourly taxes paid
    hourly_tax = gross_hourly_rate - net_hourly_income

    return {
        "Gross Annual Income": ctc,
        "Net Annual Income": net_annual_income,
        "Net Monthly Income": net_monthly_income,
        "Net Weekly Income": net_weekly_income,
        "Net Hourly Income": net_hourly_income,
        "Gross Hourly Rate": gross_hourly_rate,
        "Hourly Tax Payment": hourly_tax,
        "Federal Tax": federal_tax,
        "State Tax": state_tax,
        "City Tax": city_tax
    }

# Streamlit UI
st.title("Net Income Calculator with Progressive Taxes")

# Option for user to select state and city
state = st.selectbox("Select the state:", ["New York", "California"])
if state == "New York":
    city = st.selectbox("Select the city:", ["New York City"])
elif state == "California":
    city = st.selectbox("Select the city:", ["Bay Area"])

# Option for user to input hourly rate or annual income
option = st.radio("Would you like to input your hourly rate or annual income (CTC)?", ("Hourly Rate", "Annual Income"))

if option == "Annual Income":
    # Input for Gross Annual Income (CTC)
    ctc = st.number_input("Enter your gross annual income (CTC):", min_value=0, value=113703)

elif option == "Hourly Rate":
    # Input for hourly rate
    hourly_rate = st.number_input("Enter your hourly rate:", min_value=0.0, value=40.00)
    # Convert hourly rate to annual income assuming 40-hour workweeks and 52 weeks in a year
    ctc = hourly_rate * 40 * 52

# Button to calculate
if st.button("Calculate Net Income"):
    # Calculate net income
    results = calculate_net_income(ctc, state, city)
    
    # Display the results
    st.write(f"### Results based on an annual gross income of ${ctc:,.2f} in {city}, {state}")
    st.write(f"**Gross Annual Income:** ${results['Gross Annual Income']:,.2f}")
    st.write(f"**Net Annual Income:** ${results['Net Annual Income']:,.2f}")
    st.write(f"**Net Monthly Income:** ${results['Net Monthly Income']:,.2f}")
    st.write(f"**Net Weekly Income:** ${results['Net Weekly Income']:,.2f}")
    st.write(f"**Net Hourly Income:** ${results['Net Hourly Income']:,.2f}")
    st.write(f"**Gross Hourly Rate:** ${results['Gross Hourly Rate']:,.2f}")
    st.write(f"**Hourly Tax Payment:** ${results['Hourly Tax Payment']:,.2f}")
    
    # Display breakdown of taxes
    
    st.write(f"### Breakdown of Taxes Paid:")
    
    st.write(f"**Federal Tax:** ${results['Federal Tax']:,.2f}")
    st.write(f"**State Tax:** ${results['State Tax']:,.2f}")
    if results["City Tax"] > 0:
        st.write(f"**City Tax:** ${results['City Tax']:,.2f}")
