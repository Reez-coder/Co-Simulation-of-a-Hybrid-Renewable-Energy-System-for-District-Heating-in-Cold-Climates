# Co-Simulation of a Hybrid Renewable Energy System for District Heating in Cold Climates

[![OpenModelica](https://img.shields.io/badge/OpenModelica-1.22.0-lightgrey)](https://openmodelica.org/)
[![PYTHON](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

A smart, modular, and real-time controlled energy system designed for Swedish winters combining PV, wind, gas turbine, and battery FMUs in Python.

## Introduction

In frigid countries like Sweden, heating can account for up to **70%** of residential energy demand — especially during winter. But fossil-fueled systems pose both environmental and economic concerns under volatile weather.

This project tackles that challenge by simulating a **smart hybrid renewable energy system** that ensures:

- Constant thermal output  
- Prioritization of renewables  
- Dynamic control using a Python-based co-simulation framework  

Each subsystem — PV, Wind, Battery, Gas Turbine, Heater, Controller — is modeled in **OpenModelica**, exported as **FMUs**, and integrated in **Python** through real-time orchestration logic.

> **The result?** A smart, reactive microgrid that thinks, adapts, and heats efficiently.

## Objectives

-  Maintain **363.5 K** outlet temperature at all times  
-  Prioritize **renewable energy** (PV + Wind)  
-  Use **battery storage** to absorb surplus and supply deficit  
-  Activate **gas turbine** only when necessary  
-  Export to **grid** only when storage is full  

## System Overview

### Components

-  **PV FMU** – generates electricity based on irradiance  
-  **Wind Turbine FMU** – Complements solar generation by converting wind speed into electrical power
-  **Battery FMU** – Stores excess renewable energy and provides power during shortages
-  **Gas Turbine FMU** – dispatchable power & heat with efficiency recovery  
-  **Heater FMU** – uses electricity + recovered heat to heat water  
-  **Supervisory Controller FMU** – smart logic to dispatch power and balance constraints  

### Overview 
PV, Wind, and Gas Turbine vs Heater Demand ![](Powerprofile.png)
### Simulation Context

-  Realistic **3-day Swedish winter** with sunny, rainy, and snowy periods  
-  Inputs: 15-min interval irradiance, wind speed, ambient & water temperatures  
-  Time step: **900 seconds**

## System Parameters

### Battery
- **Maximum energy capacity**: `1.4 MWh`
- **Maximum charge/discharge power**: `400,000 W`
- **Initial state of charge (SOC)**: `0.5`
- **SOC minimum limit**: `0.20`
- **SOC maximum limit**: `0.98`

### Photovoltaic (PV)
- **Number of PV panels**: `10,000`
- **Rated panel power (STC)**: `300 W`
- **Reference irradiance**: `1000 W/m²`
- **Temperature coefficient**: `0.004 1/°C`
- **Panel efficiency**: `25%`
- **Assumed output voltage**: `24 V`

### Wind Turbine
- **Rated power**: `350,000 W`
- **Cut-in, rated, and cut-out wind speeds**: *(Model-specific)*
- **Generator efficiency**: *(Assumed ~90%)*

### Gas Turbine
- **Electrical efficiency**: `0.35`
- **Thermal (heat recovery) efficiency**: `0.45`
- **Minimum power output**: `350,000 W`
- **Maximum power output**: `1,000,000 W`

### Heater
- **Specific heat capacity of water**: `4186 J/(kg·K)`
- **Heater efficiency**: `0.95`
- **Maximum electrical power**: `11,000,000 W`
- **Setpoint outlet temperature**: `363.5 K`

### Controller
- **Control time step**: `900 s` (15 minutes)


##  How It Works
1.  The system components are modelled on open-modellica and saved as FMU files
2. All FMUs are instantiated via a Python wrapper
3. `project.py` imports component models from `myFMU` and reads data from `data.csv` 
4. Every 15-minute interval:
   - PV & Wind generate power based on weather data
   - Controller decides:
     - Gas Turbine output
     - Battery charge/discharge within SOC constraints are met
     - Grid export logic
     - Balancing renewable generation, battery use, and gas turbine support to meet heater demand
   - Heater uses power to heat water to desired temperature while respecting limits
5. Data stored in `results.csv`
6. `plottedfigures.py` generates insightful plots

---

## Plots & Analytics

By running `plottedfigures.py`, the following results were obtained:

- PV, Wind, and Gas Turbine vs Heater Demand ![](Powerprofile.png)
- Grid Export vs SOC ![](Gridexportpower.png)
- Heater Inlet/Outlet Temperature vs Time ![](Heatenergyprofile.png)
- Constraint Compliance Charts ![](Constrainschecks.png)
- SOC bounds ![](HeatControllimits.png)
- Battery SOC vs Time ![](batterySOC.png)



## Results Summary

| Metric                 | Result                          |
|------------------------|---------------------------------|
| Heater outlet temp     | Maintained at ~363.5 K          |
| PV & Wind Utilization  | Maximized                       |
| Gas Turbine Usage      | Only when needed                |
| Battery SOC Range      | Always within 0.2 – 0.98        |
| Grid Export            | Only when SOC ≥ 0.98            |
| Constraint Violations  | None                            |
| Gas Turbine Limits     | (350–1000 kW)                   |
| Battery charge/discharge   | (±400 kW)                   |


## To Run the Simulation

1. **Install dependencies**:
   ```bash
   pip install pandas matplotlib fmpy

FMUDir/systemproject/*.fmu
python project.py
python plottedfigures.py
