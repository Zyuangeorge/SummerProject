import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go

df = pd.read_csv('Cycle_Data/CHAM_26/CHAM_26_1_cycles_200.csv', header=8, usecols=['Cycle', 'AH-OUT'])

trace1 = go.Scatter(
    x = df['Cycle'],
    y = df['AH-OUT'],
    mode = "lines",
    name = "CHAM_26_1_cycles_200",
    marker = dict(color = 'rgba(16,112,2,0.8)'),
    text = 'ZW_Cham200cycles_1C.000' )

data = [trace1]

layout = dict(title = 'CHAM_26 data',
            xaxis= dict(title= 'Cycle'),
            yaxis= dict(title= 'AH-OUT'),
            legend= dict(x=1.1,y=1))

fig = dict(data = data, layout = layout)

py.iplot(fig, filename='AH-OUT/Cycle')