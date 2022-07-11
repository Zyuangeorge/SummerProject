import pandas as pd
import plotly.graph_objs as go

# read csv files
battery1_1=pd.read_csv('Cycle_Data_2/ZW_CHAM_M_2000cycles_1.csv', header=1)

df=pd.read_csv('Cycle_Data_2/ZW_CHAM_M_2000cycles_1.csv', header=1)

cycle = 1

battery1_1_filtered = df.loc[(df['Cyc#'] == cycle) & (df['Amps'] == 0)] # when amp = 0

point2 = battery1_1_filtered.head(1)
point3 = battery1_1_filtered.tail(1)
point1 = df[list(point2.index)[0]-1:list(point2.index)[0]]
point4 = df[list(point3.index)[0]+1:list(point3.index)[0]+2]

internal_resistance_1 = (point2.iat[0,8] - point1.iat[0,8]) / (point2.iat[0,7] - point1.iat[0,7])
internal_resistance_2 = (point4.iat[0,8] - point3.iat[0,8]) / (point4.iat[0,7] - point3.iat[0,7])

output = pd.DataFrame([[cycle, internal_resistance_1], [cycle, internal_resistance_2]], columns=['Cycle', 'Internal_resistance'])
print(output)


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

test_line = go.Scatter(
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
