model testHeater
  // Test inputs
  parameter Real m_flow = 1       "kg/s";
  parameter Real T_in   = 210     "K";

  // Instantiate your new Heater
  Heater heater(
    m_flow = m_flow,
    T_in   = T_in
  );

  // Outputs to inspect
  output Real P_req        = heater.P_req;
  output Real P_electrical = heater.P_electrical;
  annotation(
    experiment(StopTime = 0.1) // a single, near‐zero time for algebraic models
  );
end testHeater;
