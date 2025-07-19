model WindT
  import Modelica.Constants.pi;
  
  input Real v_wind "Wind speed (m/s)";
  input Real T_amb  "Air temperature (°C)";

  // Parameters
  parameter Real R           = 61.5     "Rotor radius (m)";
  parameter Real P_rated     = 5e5    "Rated mech. power (W)";
  parameter Real v_cut_in    = 3.0      "Cut-in speed (m/s)";
  parameter Real v_rated     = 11.4     "Rated speed (m/s)";
  parameter Real v_cut_out   = 20.0     "Cut-out speed (m/s)";
  parameter Real Cp_opt      = 0.45     "Power coefficient";
  parameter Real eta_turbine = 0.95     "Turbine efficiency";
  parameter Real p_atm       = 101325   "Std. atm. pressure (Pa)";

  // Derived
  Real A        = pi*R^2                             "Swept area (m2)";
  Real T_K      = T_amb + 273.15                     "Temp in K";
  Real rho      = p_atm/(287.05*T_K)                 "Air density (kg/m3)";

  // Outputs
  output Real P_mech "Mechanical power (W)";
  output Real P_elec "Electrical power (W)";
  output String status "Operating status";

equation 
  if v_wind < v_cut_in then
    P_mech = 0; status="Cut-in";
  elseif v_wind < v_rated then
    P_mech = 0.5*rho*A*Cp_opt*v_wind^3; status="Normal";
  elseif v_wind < v_cut_out then
    P_mech = P_rated; status="Limit";
  else
    P_mech = 0; status="Cut-out";
  end if;

  P_elec = eta_turbine*P_mech;
end WindT;
