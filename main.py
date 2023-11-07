# Code to calculate the economic viability of wind farm
import pandas as pd
from tabulate import tabulate
from calculations import *

# Data Input
print("")
print("--------------------------- DATA INPUT --------------------------------")
print("")

wf_capacity = int(input("Please, inform the wind farm capacity: ")) # Capacity of the wind farm in [MW]
ci = float(input("Please, inform the capital of investment: ")) # Capital of investment applied on the wind farm [euros]
period_years = int(input("Please, inform the period of years: ")) # Period of years
decommissioning_costs = float(input("Please, inform the Decommissioning costs: ")) # Decommisioning costs [euros]
ope_main_costs = float(input("Please, inform the operating and maintenance cost: ")) # Annual cost of operating and maintenance [euro/kWh]
annual_energy_prod = float(input("Please, inform the annual energy production: ")) # Annual energy production [kWh]
elec_selling_price = float(input("Please, inform the price of selling the electricity: ")) # Electricity selling price - "tariff" [euro/kWh]
annual_rate = float(input("Please, inform the annual discount rate: ")) # Annual discount rate [%]


# Processing of Data
OM_costs_year = AnnualOperatingMaintenanceCost(annual_energy_prod, ope_main_costs)

annual_revenue = AnnualRevenue(annual_energy_prod, elec_selling_price)

annual_net_income = AnnualNetIncome(annual_revenue, OM_costs_year)

net_present_value = NetPresentValue(annual_net_income, annual_rate, period_years, ci)

present_value_maintenance = PresentValueMaintenance(OM_costs_year, annual_rate, period_years)

present_value_costs_deco = PresentValueDecommisioning(decommissioning_costs, annual_rate, period_years)

present_value_all_costs = PresentValueAllCosts(present_value_costs_deco, present_value_maintenance, ci)

levellised_annual_cost = LevellisedAnnualCost(present_value_all_costs, annual_rate, period_years)

levellised_cost_energy = LevellisedCostEnergy(levellised_annual_cost, annual_energy_prod)

# Results of calculation
print("")
print("--------------------------- RESULTS OF CALCULATION --------------------------------")
print("")

print(f"Annual operating and maintenance cost = {OM_costs_year.calculate():.2f} euros")
print(f"Annual revenue from selling the electricity = {annual_revenue.calculate():.2f} euros")
print(f"Annual Net Income = {annual_net_income.calculate():.2f} euros")
print(f"Net Present Value = {net_present_value.calculate():.2f} euros")
print(f"Present value maintenance and repair cost = {present_value_maintenance.calculate():.2f} euros")
print(f"Present value of the cost of decommissioning = {present_value_costs_deco.calculate():.2f} euros")
print(f"Present value of all the costs = {present_value_all_costs.calculate():.2f} euros")
print(f"Levellised annual costs = {levellised_annual_cost.calculate():.2f} euros")
print(f"Levellised cost of energy = {levellised_cost_energy.calculate():.4f} euros/kWh")

print("")

data = {
    "Parameter": ["Annual operating and maintenance cost", "Annual revenue from selling the electricity", "Annual Net Income", "Net Present Value", "Present value maintenance and repair cost", "Present value of the cost of decommissioning", "Present value of all the costs", "Levellised annual costs", "Levellised cost of energy"],
    "Results": [f"{OM_costs_year.calculate():.2f}", annual_revenue.calculate(), annual_net_income.calculate(), net_present_value.calculate(), present_value_maintenance.calculate(), present_value_costs_deco.calculate(), present_value_all_costs.calculate(), levellised_annual_cost.calculate(), levellised_cost_energy.calculate()]
}

df = pd.DataFrame(data)

print(tabulate(df, headers='keys', tablefmt='grid'))