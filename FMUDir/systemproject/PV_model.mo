model PV_model
  parameter Real n_pv = 1;             // number of panels
  parameter Real PV_eff = 0.25;        // panel efficiency (25%)
  parameter Real p_stc = 300;          // rated power under STC (W)
  parameter Real irr_stc = 1000;       // standard irradiance (W/m²)
  parameter Real t_stc = 25;           // standard temperature (°C)
  parameter Real c_t = 0.004;          // temperature coefficient
  parameter Real Vpv = 24;
  
  input Real Irr;                      // real-time irradiance (W/m²)
  input Real Temp;                     // real-time temperature in Kelvins
  output Real P_pv;                    // PV power output (W)

equation
  P_pv = n_pv * PV_eff * p_stc * (Irr / irr_stc) * (1 - c_t * ((Temp-273.15) - t_stc));
end PV_model;


