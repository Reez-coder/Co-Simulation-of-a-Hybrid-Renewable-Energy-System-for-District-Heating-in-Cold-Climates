model GasTurbine
  input Real P_CCreq "[W]";  
  input Real T_amb   "[K]"; 

  output Real P_CC   "[W]"; 
 
  parameter Real eff_electrical = 0.35;
  parameter Real eff_thermal = 0.45;
  parameter Real P_min = 350e3 "[W]"; 
  parameter Real P_max = 1e6   "[W]"; 

protected
  Real P_requested;

equation 
  // Clamp request between min and max
  P_requested = min(P_max, max(P_min, P_CCreq));

  // Derate based on ambient temperature
  P_CC = if P_CCreq > 0 then P_requested * (1 - 0.0015 * (T_amb - 298)) else 0;

end GasTurbine;
