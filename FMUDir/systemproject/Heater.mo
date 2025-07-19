model Heater
  input Real m_flow;
  input Real T_in;

  parameter Real cp_water = 4186;
  parameter Real P_max = 11e6;
  parameter Real eta = 0.95;
  parameter Real T_setpoint = 363.5;

  output Real P_req;
  output Real P_electrical;
equation
  P_req = m_flow * cp_water * (T_setpoint - T_in);
  P_electrical = P_req/eta;
end Heater;
