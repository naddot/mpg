import streamlit as st

def calculate_fuel_costs_by_grade(fuel_consumption_mpg, annual_mileage, fuel_price):
    """
    Compare fuel costs across all tyre grades (A to E) based on RRC values.
    
    Parameters:
    - fuel_consumption_mpg (float): Fuel consumption in MPG (UK miles per gallon).
    - annual_mileage (float): Distance driven per year in miles.
    - fuel_price (float): Fuel price per litre.
    
    Returns:
    - cost_differences (dict): Dictionary of fuel cost differences relative to A-rated tyres.
    - percentage_increase (dict): Percentage increase in fuel costs relative to A-rated tyres.
    """
    
    # Conversion factors
    mpg_to_l_per_100km = 282.48  # 1 MPG (UK) = 282.48 / L/100km
    miles_to_km = 1.60934
    
    # Convert MPG to L/100km
    base_fuel_consumption_l_per_100km = mpg_to_l_per_100km / fuel_consumption_mpg
    
    #convert pence to pounds
    fuel_price = fuel_price/100
    
    # Tyre grades and corresponding RRC values
    tyre_grades = {
        "A": 6.5,
        "B": 7.2,
        "C": 8.4,
        "D": 9.8,
        "E": 11.0
    }
    
    # Fuel savings per 10% RRC increase: estimated 1-2% increase in fuel consumption
    fuel_savings_rate = 0.015  # Midpoint of 1-2% range per 10% RRC change
    
    # Calculate cost for A-rated tyre as baseline
    base_fuel_per_year_l = (base_fuel_consumption_l_per_100km / 100) * (annual_mileage * miles_to_km)
    base_fuel_cost = base_fuel_per_year_l * fuel_price
    
    cost_differences = {"A": 0.00}  # A-rated tyre is the baseline, so £0 difference
    percentage_increase = {"A": 0.00}  # A-rated tyre as baseline (0% increase)
    
    for grade, rrc in tyre_grades.items():
        if grade == "A":
            continue
        
        # Percentage increase in RRC relative to A-rated tyre
        rrc_increase_percentage = (rrc - tyre_grades["A"]) / tyre_grades["A"] * 100
        
        # Estimated increase in fuel consumption
        fuel_increase_percentage = fuel_savings_rate * (rrc_increase_percentage / 10)
        
        # New fuel consumption in L/100km
        new_fuel_consumption_l_per_100km = base_fuel_consumption_l_per_100km * (1 + fuel_increase_percentage)
        
        # New annual fuel consumption and cost
        new_fuel_per_year_l = (new_fuel_consumption_l_per_100km / 100) * (annual_mileage * miles_to_km)
        new_fuel_cost = new_fuel_per_year_l * fuel_price
        
        # Cost difference compared to A-rated tyre
        cost_difference = new_fuel_cost - base_fuel_cost
        cost_differences[grade] = cost_difference
        
        # Percentage increase relative to A-rated tyre
        percentage_increase[grade] = (cost_difference / base_fuel_cost) * 100
    
    return cost_differences, percentage_increase

# Streamlit Web App
st.set_page_config(layout="wide")

st.title("Tyre Rolling Resistance Fuel Cost Calculator")

col1, col2 = st.columns([2, 1])

with col1:
    fuel_consumption_mpg = st.number_input("Enter your vehicle's MPG (UK):", min_value=1.0, value=40.0)
    annual_mileage = st.number_input("Enter your average annual mileage (miles):", min_value=1.0, value=12000.0)
    fuel_price = st.number_input("Enter the current fuel price per litre (£):", min_value=0.1, value=1.60)

    if st.button("Calculate Fuel Costs"):
        cost_differences, percentage_increase = calculate_fuel_costs_by_grade(fuel_consumption_mpg, annual_mileage, fuel_price)
        
        st.write("\n### Fuel cost differences by tyre grade (compared to A-rated tyres):")
        for grade in cost_differences:
            st.write(f"**{grade}-rated:** £{cost_differences[grade]:.2f} (+{percentage_increase[grade]:.2f}%)")

with col2:
    st.markdown("## About Rolling Resistance")
    st.write(
        f"Lowering the rolling resistance of passenger car tires leads to measurable fuel savings."
        f"Industry experiments (Michelin and TNO projects) all quantify the benefit at roughly 1% fuel saved per 5–10% reduction in RRC, or about 2% fuel economy improvement for a 0.001 decrease in RRC for the average car. "
        f"Simply by choosing tires and road designs that minimise rolling resistance you can save fuel and make meaningful CO₂ reductions over time"
    )
