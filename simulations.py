import numpy as np

def simulate_wealth(config: dict) -> tuple[np.ndarray, list[float]]:
    """
    Simulates wealth development over time based on input parameters.
    Returns:
        - numpy array of ages
        - list of wealth values over time
    """
    # Time variables
    years = config["simulation_years"]
    current_age = config["start_age"]
    retirement_age = config["retirement_age"]
    end_age = current_age + years

    # Financial variables
    wealth = [config["initial_wealth"]]
    income = config["annual_income"]
    savings_rate = config["savings_rate"]
    return_rate = config["expected_return"]
    inflation = config["inflation_rate"]

    for age in range(current_age, end_age):
        # Only save while working
        if age < retirement_age:
            savings = income * savings_rate
        else:
            savings = 0

        # Update wealth with savings and net return
        new_wealth = (wealth[-1] + savings) * (1 + return_rate - inflation)
        wealth.append(new_wealth)

    # Create array of ages
    age_range = np.arange(current_age, current_age + years + 1)

    return age_range, wealth

