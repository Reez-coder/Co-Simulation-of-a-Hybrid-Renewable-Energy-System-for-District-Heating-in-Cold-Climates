from myFMU.myFMU import myFMU
import pandas as pd

fmuDirw="FMUDir/" # windows architecture
rep="systemproject/"
path= fmuDirw+rep

controllerfile="lo.fmu"
heaterfile="Heater.fmu"
windfile = "WindT.fmu"
pvfile ="PV_model.fmu"
gastfile ="GasTurbine.fmu"
batfile= "BatteryModel.fmu"

controllerfmu=path+controllerfile
heaterfmu=path+heaterfile
gastfmu=path+gastfile
pvfmu=path+pvfile
batfmu=path+batfile
windfmu  = path + windfile

import numpy as np


def simulate_energy_system(csv_path, mflow_const=1.0):
    # Load and clean column names
    data = pd.read_csv(csv_path)
    data.columns = data.columns.str.strip()
    data.rename(columns={
        'Irr':    'Irr',
        'S_wind': 'v_wind',
        'Tamb':   'T_amb',
        'Twater': 'T_water'
    }, inplace=True)

    # Extract series
    n = len(data)
    irr_series    = data['Irr'].values
    vwind_series  = data['v_wind'].values
    tamb_series   = data['T_amb'].values
    twater_series = data['T_water'].values
    mflow_series  = np.full(n, mflow_const)

    # Instantiate FMUs
    Fcontroller = myFMU(controllerfmu)
    Fbat        = myFMU(batfmu)
    Fheater     = myFMU(heaterfmu)
    Fgast       = myFMU(gastfmu)
    Fpv         = myFMU(pvfmu)
    Fwind       = myFMU(windfmu)

    # Initialize simulation
    t      = 0.0
    deltaT = 900.0

    Fcontroller.init(t, [])
    Fbat.init(t, [('SOC', 0.5), ('P_bat', 0.0)])  
    Fheater.init(t, [])
    Fgast.init(t, [])
    Fpv.init(t, [('n_pv', 10000)])
    Fwind.init(t, [('P_rated', 350000)])
    # Prepare results container
    results = {key: [] for key in (
        'time', 'Irr', 'v_wind', 'T_amb', 'T_water',
        'P_elec_wind',
        'P_pv',
        'P_req', 'Q_provided', 'T_in', 'T_out',
        'SOC', 'P_CCreq', 'P_bat', 'P_export',
        'P_CC', 'Q_heat'
    )}

    # Simulation loop
    q_heat = 0.0
        # --- Initialize loop variables so they exist on iter=0 ---  ## <<< init
    p_req = 0.0                                               ## <<< init
    p_bat = 0.0                                               ## <<< init
    soc   = 0.5  
    for i in range(n):
        irr   = irr_series[i]
        vwind = vwind_series[i]
        Ta    = tamb_series[i]
        Tw    = twater_series[i]
        mf    = mflow_series[i]

        # Wind turbine
        Fwind.set(['T_amb','v_wind'], [Ta, vwind])
        Fwind.doStep(t, deltaT)
        p_elec_wind = Fwind.get('P_elec')

        # PV
        Fpv.set(['Irr','Temp'], [irr, Ta - 273.15])
        Fpv.doStep(t, deltaT)
        p_pv = Fpv.get('P_pv')

        # Battery update
        Fbat.set('P_bat', p_bat)
        Fbat.doStep(t, deltaT)
        soc = Fbat.get('SOC')

        ## <<< CHANGE: compute max battery discharge capacity this step (W)
        P_bat_max = 400000.0  
        P_available_bat = max(0.0, (soc - 0.2) * (1.4e6 * 3600) / deltaT)  
        P_available_bat = min(P_available_bat, P_bat_max)
        ## <<< END CHANGE

        # Dispatch (“lo” FMU) with all five inputs
        Fcontroller.set(
            ['P_pv','P_wind','SOC_bat','P_available_bat','P_req'],
            [p_pv, p_elec_wind, soc, P_available_bat, p_req]
        )
        Fcontroller.doStep(t, deltaT)
        p_ccreq = Fcontroller.get('P_CCreq')
        p_bat   = Fcontroller.get('P_bat')
        p_exp   = Fcontroller.get('P_export')

        # Gas turbine
        Fgast.set(['P_CCreq','T_amb'], [p_ccreq, Ta])
        Fgast.doStep(t, deltaT)
        p_cc   = Fgast.get('P_CC')
        q_heat = Fgast.get('Q_heat')

        # Heater
        Fheater.set(['T_in','m_flow','Q_heat'], [Tw, mf, q_heat])
        Fheater.doStep(t, deltaT)
        p_req      = Fheater.get('P_req')
        q_provided = Fheater.get('Q_provided')
        t_out      = Fheater.get('T_out')

        # Store results
        results['time']         .append(t)
        results['Irr']          .append(irr)
        results['v_wind']       .append(vwind)
        results['T_amb']        .append(Ta)
        results['T_water']      .append(Tw)
        results['P_elec_wind']  .append(p_elec_wind)
        results['P_pv']         .append(p_pv)
        results['P_req']        .append(p_req)
        results['Q_provided']   .append(q_provided)
        results['T_in']         .append(Tw)
        results['T_out']        .append(t_out)
        results['SOC']          .append(soc)
        results['P_CCreq']      .append(p_ccreq)
        results['P_bat']        .append(p_bat)
        results['P_export']     .append(p_exp)
        results['P_CC']         .append(p_cc)
        results['Q_heat']       .append(q_heat)

        t += deltaT

    return pd.DataFrame(results)


csv_path = "data.csv"
df = simulate_energy_system(csv_path)
df.to_csv('results.csv', index=False)   # save full results

import matplotlib.pyplot as plt

plt.figure()
plt.plot(df['time'], df['SOC'])
plt.xlabel('Time (s)')
plt.ylabel('State of Charge (SOC)')
plt.title('Battery SOC Over Time')
plt.legend(['SOC'])
plt.show()

plt.figure()
plt.plot(df['time'], df['P_elec_wind'], label='P_elec_wind')
plt.plot(df['time'], df['P_CCreq'],      label='P_CCreq')
plt.plot(df['time'], df['P_pv'],          label='P_pv')
plt.plot(df['time'], df['P_req'],         label='P_req')
plt.plot(df['time'], df['P_bat'],         label='P_bat')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.title('Power Profiles Over Time')
plt.legend()
plt.show()
