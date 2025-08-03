import yaml
import streamlit as st
import pandas as pd
import plotly.express as px
from simulations import simulate_wealth

# Set up the Streamlit page
st.set_page_config(page_title="Finance Planner", layout="wide")
st.title("Finance Planner")

# Load simulation parameters from YAML file
with open("params.yml", "r") as f:
    base_config = yaml.safe_load(f)

# Load return scenarios from configuration
return_scenarios = base_config.get("return_scenarios", {})

# Run one or more simulations depending on the presence of scenarios
if not return_scenarios:
    st.warning("No return scenarios defined in params.yml. Using default expected_return.")

    ages, wealth = simulate_wealth(base_config)
    df = pd.DataFrame({"Age": ages, "Wealth (€)": wealth, "Scenario": "Default"})
else:
    dataframes = []

    for label, rate in return_scenarios.items():
        config = base_config.copy()
        config["expected_return"] = rate
        ages, wealth = simulate_wealth(config)
        df = pd.DataFrame({
            "Age": ages,
            "Wealth (€)": wealth,
            "Scenario": label
        })
        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)

# Create the plot with scenario comparison
fig = px.line(
    df,
    x="Age",
    y="Wealth (€)",
    color="Scenario",
    title="Wealth Over Time – Scenario Comparison"
)

# Add vertical line for retirement age
retirement_age = base_config["retirement_age"]
fig.add_vline(
    x=retirement_age,
    line_width=2,
    line_dash="dash",
    line_color="grey"
)

# Add dummy trace for retirement legend entry
fig.add_scatter(
    x=[None],
    y=[None],
    mode="lines",
    line=dict(color="grey", dash="dash"),
    name="Retirement age"
)

# Enable gridlines
fig.update_layout(
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Display the current simulation parameters
st.subheader("Simulation Parameters")
st.json(base_config)



