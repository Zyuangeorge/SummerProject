import plotly
import pandas as pd
import plotly.graph_objs as go

data1 = pd.read_csv('Cycle_Data/CHAM_26/CHAM_26_1_cycles_200.csv', header=8)
data2 = pd.read_csv('Cycle_Data/CHAM_26/CHAM_26_2_cycles_200.csv', header=8)

""" print(data1.head())
print(data2.head()) """

line1 = go.Scatter(
    x=data1['Cycle'], 
    y=data1['AH-OUT'], 
    name='CHAM_26_1', 
    marker_color='rgb(255,0,0)')

line2 = go.Scatter(
    x=data2['Cycle'], 
    y=data2['AH-OUT'], 
    name='CHAM_26_2', 
    marker_color='rgb(255,0,0)', 
    line = dict(dash='dash'))

fig = go.Figure([line1,line2])

fig.update_layout(
    title = 'CHAM_26_cycles_200 Battery 1 and Battery 2 Data',
    xaxis_title = 'Cycle',
    yaxis_title = 'AH-OUT'
)

fig.show()

""" data = [line] """

""" layout = dict(title = 'CHAM_26 data',
            xaxis= dict(title= 'Cycle'),
            yaxis= dict(title= 'AH-OUT'),
            legend= dict(x=1.1,y=1)) """

""" fig = dict(data = data, layout = layout) """

""" py.iplot(fig, filename='AH-OUT/Cycle') """