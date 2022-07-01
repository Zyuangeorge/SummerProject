import pandas as pd
import plotly.graph_objs as go

# read csv files
battery1_1=pd.read_csv('Cycle_Data_2/ZW_CHAM_M_2000cycles_1.csv', header=1)

# Set the curves
amp_line = go.Scatter(
    x=battery1_1['Rec#'], 
    y=battery1_1['Amps'], 
    name='amp_line', 
    marker_color='rgb(0,255,0)')

volt_line = go.Scatter(
    x=battery1_1['Rec#'], 
    y=battery1_1['Volts'], 
    name='volt_line', 
    marker_color='rgb(255,0,0)')

# Plot the curves
fig = go.Figure([amp_line,volt_line])

fig.update_layout(
    title = 'CHAM_26 Battery 1 and Battery 2 Amps/Rec# Data',
    xaxis_title = 'Rec#',
    yaxis_title = 'Amps (Ah),Volts (V)',
    hovermode='x unified'
)

fig.show()
