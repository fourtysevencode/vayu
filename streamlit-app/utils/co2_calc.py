emission_factors = {
    "bike": 0.05,
    "car": 0.21,
    "bus": 0.089,
    "metro": 0.031,
    "auto": 0.065
}

diet_co2 = {"nonveg": 120, "veg": 55, "eggatarian (mmm eggs)": 80}

waste_co2 = {
    "none (im insane)": 0,
    "very low": 2,
    "low": 4,
    "medium": 9,
    "high": 13,
    "very high": 16,
    "new landfills are created because of me": 18
}

def co2_calc(mode_of_transport, commute_distance, electricity_usage, lpg_cylinders, diet, waste):
    transport = commute_distance * 2 * 22 * emission_factors[mode_of_transport]
    electricity = electricity_usage * 0.82 # india average CO2 her unit (kwh)
    lpg = lpg_cylinders * 29.5 # india average CO2 per can
    food = diet_co2[diet]
    trash = waste_co2[waste]

    total = transport + electricity + lpg + food + trash

    return total