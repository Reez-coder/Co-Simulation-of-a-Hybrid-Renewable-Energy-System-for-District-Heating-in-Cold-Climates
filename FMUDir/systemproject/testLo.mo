 model TestHeaterDispatch
    Real P_wind = 250e3;
    Real T_water_test = 250;
    Real m_flow = 1.0; // for example, in kg/s
    Real Irr =  500e3 * (1 + 0.2 * sin(2 * Modelica.Constants.pi * time)); // vary with time
    Real T_amb = 301;

    // Instantiate components
    Heater        h;
    lo            disp;
    BatteryModel  bat;
    PV_model pva;
    GasTurbine GT;


  equation
    // Dispatch inputs ( and SOC)
    
    GT.T_amb = T_amb;
    GT.P_CCreq = disp.P_CCreq;
    pva.Irr = Irr;
    pva.Temp = T_amb; 
    h.m_flow = 1.0; 
    h.T_in = T_water_test;
    h.Q_heat = GT.Q_heat;
    disp.P_pv = pva.P_pv;
    disp.P_wind          = P_wind;
    disp.P_req           = h.P_req;
    disp.SOC_bat         = bat.SOC;
    bat.P_bat = disp.P_bat;
annotation (experiment(
    StartTime = 0,
    StopTime  = 86400,
    Interval  = 3600));
end TestHeaterDispatch;

