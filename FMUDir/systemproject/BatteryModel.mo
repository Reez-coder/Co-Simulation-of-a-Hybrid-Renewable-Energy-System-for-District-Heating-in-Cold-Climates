model BatteryModel
  // Parámetros
  parameter Real E_max    = 1.4e6*3600  "J";
  parameter Real SOC_min  = 0.2;
  parameter Real SOC_max  = 0.98;

  // Entrada y salida
  input  Real P_bat       "Solicitado >0=carga, <0=descarga [W]";
  output Real SOC         "State of charge [0–1]";

equation
  // Dinámica de SOC (evita salirse de [min,max])
  der(SOC) = if (SOC<=SOC_min and P_bat<0) or (SOC>=SOC_max and P_bat>0)
             then 0
             else P_bat/E_max;

initial equation
  SOC = 0.5;
end BatteryModel;
