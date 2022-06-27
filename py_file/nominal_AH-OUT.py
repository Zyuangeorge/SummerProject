import os
import pandas as pd
import plotly.graph_objects as go

# ====================CHAM_26====================
# Set the path and path list of the folder
CHAM_26_path = 'Cycle_Data/CHAM_26/'
files = os.listdir(CHAM_26_path)

# Filter out other files
CHAM_26_1_files = list(
    filter(lambda x: (x[0:9] == 'CHAM_26_1' and x[-4:] == '.csv'), files))
CHAM_26_2_files = list(
    filter(lambda x: (x[0:9] == 'CHAM_26_2' and x[-4:] == '.csv'), files))

# Read the file to file list and sort the list based on the time information
CHAM_26_1_list = []
for file in CHAM_26_1_files:
    tmp = pd.read_csv(CHAM_26_path + file, header=8)
    CHAM_26_1_list.append(tmp)
CHAM_26_1_list = sorted(CHAM_26_1_list, key=lambda k: k['Date'][0])

CHAM_26_2_list = []
for file in CHAM_26_2_files:
    tmp = pd.read_csv(CHAM_26_path + file, header=8)
    CHAM_26_2_list.append(tmp)
CHAM_26_2_list = sorted(CHAM_26_2_list, key=lambda k: k['Date'][0])

# Merge the data in the list to one dataframe variable and create a new series called AH-OUT-NOMINAL
dataset_CHAM_26_1 = pd.concat(
    CHAM_26_1_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_CHAM_26_1)):
    dataset_CHAM_26_1.loc[data, 'Cycle'] = data

dataset_CHAM_26_1['AH-OUT-NOMINAL'] = dataset_CHAM_26_1.apply(
    lambda x: x['AH-OUT'] / dataset_CHAM_26_1.loc[0, 'AH-OUT'], axis=1)

dataset_CHAM_26_2 = pd.concat(
    CHAM_26_2_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_CHAM_26_2)):
    dataset_CHAM_26_2.loc[data, 'Cycle'] = data

dataset_CHAM_26_2['AH-OUT-NOMINAL'] = dataset_CHAM_26_2.apply(
    lambda x: x['AH-OUT'] / dataset_CHAM_26_2.loc[0, 'AH-OUT'], axis=1)

# Plot the curves
line_CHAM_26_1 = go.Scatter(x=dataset_CHAM_26_1['Cycle'],
                            y=dataset_CHAM_26_1['AH-OUT-NOMINAL'],
                            name='CHAM_26_1',
                            marker_color='rgb(255,0,0)')

line_CHAM_26_2 = go.Scatter(x=dataset_CHAM_26_2['Cycle'],
                            y=dataset_CHAM_26_2['AH-OUT-NOMINAL'],
                            name='CHAM_26_2',
                            marker_color='rgb(255,0,0)',
                            line=dict(dash='dash'))


# ====================Plot codes====================

# Combine the curves to one figure
fig = go.Figure([line_CHAM_26_1,line_CHAM_26_2,])

# Config the layout
fig.update_layout(
    title='Battery AH-OUT-NOMINAL/Cycle Data',
    xaxis_title='Cycle',
    yaxis_title='AH-OUT-NOMINAL',
    hovermode='x'
)

fig.show()
