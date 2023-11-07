# Classes to perform calculations
class AnnualOperatingMaintenanceCost(object):
    """
    Class that calculates annual operation and maintenance costs.
    """

    def __init__(self, energy_prod_annual, ope_main_cost):
        self.__energy_prod_annual = energy_prod_annual
        self.__ope_main_cost = ope_main_cost

    def calculate(self):
        annual_ope_main_cost = self.__energy_prod_annual * self.__ope_main_cost
        return annual_ope_main_cost
    
class AnnualRevenue(object):
    """
    Class that calculates annual revenue from total energy production times the energy sales price
    """

    def __init__(self, annual_energy_prod, elec_sell_price):
        self.__annual_energy_prod = annual_energy_prod
        self.__elec_sell_price = elec_sell_price

    def calculate(self):
        annual_revenue = self.__annual_energy_prod * self.__elec_sell_price
        return annual_revenue
    
class AnnualNetIncome(object):
    """
    Class that calculates net profit from the difference between annual revenue and operation and maintenance costs
    """

    def __init__(self, annual_revenue: AnnualRevenue, annual_ope_main_cost: AnnualOperatingMaintenanceCost):
        self.__annual_revenue = annual_revenue
        self.__annual_ope_main_cost = annual_ope_main_cost

    def calculate(self):
        annual_net_income = self.__annual_revenue.calculate() - self.__annual_ope_main_cost.calculate()
        return annual_net_income
    
class NetPresentValue(object):
    """
    Class that calculates the net present value of a specific quantity based on the annual rate, the period in years and the investment capital
    """

    def __init__(self, annual_net_income: AnnualNetIncome, annual_rate, period_years, capital_investment):
        self.__annual_net_income = annual_net_income
        self.__annual_rate = annual_rate
        self.__period_years = period_years
        self.__capital_investment = capital_investment

    def calculate(self):
        npv = 0
        for p in range(1, self.__period_years+1):
            npv += ((self.__annual_net_income.calculate())/((1+(self.__annual_rate/100))**p))
        npv -= self.__capital_investment
        return npv
    
class PresentValueMaintenance(object):
    """
    Class that calculates the present value of maintenance based on the annual rate and the period in years
    """

    
    def __init__(self, annual_ope_man, annual_rate, period_years):
        self.__annual_ope_man = annual_ope_man
        self.__annual_rate = annual_rate
        self.__period_years = period_years

    def calculate(self):
        pvm = 0
        for p in range(1, self.__period_years+1):
            pvm += ((self.__annual_ope_man.calculate())/((1+(self.__annual_rate/100))**p))
        return pvm

class PresentValue(object):
    """
    Class that calculates the present value from a future value, taking into account the annual rate and the period in years.
    """

    def __init__(self, future_value, annual_rate, period_years):
        self.__future_value = future_value
        self.__annual_rate = annual_rate
        self.__period_years = period_years

    def calculate(self):
        present_value = self.__future_value * (1/((1+(self.__annual_rate/100))**self.__period_years))
        return present_value
    
class PresentValueDecommisioning(PresentValue):
    """
    Class that uses the 'PresentValue' class to calculate the present value based on the commission rate.
    """

    def __init__(self, future_value, annual_rate, period_years):
        super().__init__(future_value, annual_rate, period_years)

class PresentValueAllCosts(object):
    """
    Class that calculates the present value of aggregate costs, such as: decommissioning cost, maintenance cost and cost related to investment capital.
    """

    def __init__(self, decommisioning: PresentValueDecommisioning, maintenance: PresentValueMaintenance, capital_investment: float):
        self.__decommisioning = decommisioning
        self.__maintenance = maintenance
        self.__capital_investment = capital_investment

    def calculate(self):
        pvc = self.__decommisioning.calculate() + self.__maintenance.calculate() + self.__capital_investment
        return pvc
    
class LevellisedAnnualCost(object):
    """
    Class that calculates the levelized annual cost from the annual rate and the period in years.
    """

    def __init__(self, present_value_costs: PresentValueAllCosts, annual_rate: float, period_years: int):
        self.__present_value_costs = present_value_costs
        self.__annual_rate = annual_rate
        self.__period_years = period_years

    def calculate(self):
        lac = (self.__present_value_costs.calculate()*(self.__annual_rate/100)) / (1-((1+(self.__annual_rate/100))**(-self.__period_years)))
        return lac
    
class LevellisedCostEnergy(object):
    """
    Class that calculates the levelized cost of energy from levelized costs and annual energy production.
    """

    def __init__(self, lev_annual_cost: LevellisedAnnualCost, annual_energy_prod: float):
        self.__lev_annual_cost = lev_annual_cost
        self.__annual_energy_prod = annual_energy_prod

    def calculate(self):
        lcoe = self.__lev_annual_cost.calculate() / self.__annual_energy_prod
        return lcoe