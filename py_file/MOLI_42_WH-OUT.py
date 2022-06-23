import pandas as pd
import plotly.graph_objs as go

battery1_1=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_200.csv', header=8)
battery1_2=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_400.csv', header=8)
battery1_3=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_600.csv', header=8)
battery1_4=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_800.csv', header=8)
battery1_5=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_1000.csv', header=8)
battery1_6=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_1200.csv', header=8)
battery1_7=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_1400.csv', header=8)
battery1_8=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_1600.csv', header=8)
battery1_9=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_1800.csv', header=8)
battery1_10=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_2000.csv', header=8)
battery1_11=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_1_cycles_2200.csv', header=8)

battery2_1=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_200.csv', header=8)
battery2_2=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_400.csv', header=8)
battery2_3=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_600.csv', header=8)
battery2_4=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_800.csv', header=8)
battery2_5=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_1000.csv', header=8)
battery2_6=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_1200.csv', header=8)
battery2_7=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_1400.csv', header=8)
battery2_8=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_1600.csv', header=8)
battery2_9=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_1800.csv', header=8)
battery2_10=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_2000.csv', header=8)
battery2_11=pd.read_csv('Cycle_Data/MOLI_42/MOLI_42_2_cycles_2200.csv', header=8)

data1 = pd.concat(objs=[battery1_1,
                        battery1_2,
                        battery1_3,
                        battery1_4,
                        battery1_5,
                        battery1_6,
                        battery1_7,
                        battery1_8,
                        battery1_9,
                        battery1_10,
                        battery1_11],
                        axis=0,join='outer', ignore_index=True)

data2 = pd.concat(objs=[battery2_1,
                        battery2_2,
                        battery2_3,
                        battery2_4,
                        battery2_5,
                        battery2_6,
                        battery2_7,
                        battery2_8,
                        battery2_9,
                        battery2_10,
                        battery2_11],
                        axis=0,join='outer',ignore_index=True)

for data in range(len(data1)):
    data1.loc[data,'Cycle'] = data

for data in range(len(data2)):
    data2.loc[data,'Cycle'] = data

line1 = go.Scatter(
    x=data1['Cycle'], 
    y=data1['WH-OUT'], 
    name='MOLI_42_1', 
    marker_color='rgb(0,255,0)')

line2 = go.Scatter(
    x=data2['Cycle'], 
    y=data2['WH-OUT'], 
    name='MOLI_42_2', 
    marker_color='rgb(0,255,0)', 
    line = dict(dash='dash'))

fig = go.Figure([line1,line2])

fig.update_layout(
    title = 'MOLI_42 Battery 1 and Battery 2 WH-OUT/Cycle Data',
    xaxis_title = 'Cycle',
    yaxis_title = 'WH-OUT(Wh)',
    yaxis_range = [0,15],
    hovermode='x unified'
)

fig.show()
