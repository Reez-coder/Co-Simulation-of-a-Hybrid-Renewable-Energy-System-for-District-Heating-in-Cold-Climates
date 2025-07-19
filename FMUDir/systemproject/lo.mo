model lo
  input Real P_pv "PV generation [kW]";
  input Real P_wind "Wind generation [kW]";
  input Real SOC_bat "Battery state of charge [0–1]";
  input Real P_req   (start=0,    fixed=true) "Heater power demand [kW]";
  parameter Real SOC_max    = 0.95;
  parameter Real SOC_min    = 0.20;
  parameter Real P_CC_min   = 350e3;
  parameter Real P_CC_max   = 1000e3;
  parameter Real E_max    = 1.4e6*3600  "kWh";   // convert J → kWh
  parameter Real P_bat_max = 400e3  "kW";

  output Real P_bat    "Battery power (positive = charge, negative = discharge) [kW]";
  output Real P_CCreq  "Gas turbine power output [kW]";
  output Real P_export "Grid export power [kW]";

protected
  Real P_renewable "Total renewable power [kW]";
  Real Surplus;
  Real P_remaining;
  Real extra;
  Real P_available "Battery discharge limit [kW]";

equation
  P_renewable = P_pv + P_wind;

  /* energy above SOC_min [kWh] → kW for a one-hour time-step */
  P_available = min(P_bat_max, max(0, (SOC_bat - SOC_min) * E_max));
algorithm
  P_bat := 0;
  P_CCreq := 0;
  P_export := 0;
  Surplus := 0;
  P_remaining := 0;
  extra := 0;

  if P_renewable >= P_req then
    Surplus := P_renewable - P_req;
    if SOC_bat < SOC_max then
      P_bat := Surplus;
    else
      P_export := Surplus;
    end if;
  else
    P_remaining := P_req - P_renewable;
    if SOC_bat > SOC_min then
      P_bat := -min(P_remaining, P_available);
      P_remaining := P_remaining + P_bat;
    end if;
    if P_remaining > 0 then
      P_CCreq := max(min(P_remaining, P_CC_max), P_CC_min);
      extra := P_CCreq - P_remaining;
      if extra > 0 then
          P_export := extra;
      end if;
    end if;
  end if;
end lo;
