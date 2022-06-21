import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('Cycle_Data/CHAM_26/CHAM_26_1_cycles_200.csv')

""" trace1 = go.Scatter(
    x = df['Cycle'],
    y = df['AH-OUT'],
    mode = "lines",
    name = "CHAM_26_1_cycles_200",
    marker = dict(color = 'rgba(16,112,2,0.8)'),
    text = df['TestName'] )

data = [trace1]

layout = dict(title = 'CHAM_26 data',
            xaxis= dict(title= 'Cycle',ticklen= 5,zeroline= False),
            yaxis= dict(title= 'AH-OUT',ticklen= 5,zeroline= False) )

fig = dict(data = data, layout = layout)

df.iplot(fig) """