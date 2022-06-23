import os
import pandas as pd
import plotly.graph_objects as go

# ====================CHAM_26====================
CHAM_26_path = 'Cycle_Data/CHAM_26/'
files = os.listdir(CHAM_26_path)

CHAM_26_1_files = list(
    filter(lambda x: (x[0:9] == 'CHAM_26_1' and x[-4:] == '.csv'), files))
CHAM_26_2_files = list(
    filter(lambda x: (x[0:9] == 'CHAM_26_2' and x[-4:] == '.csv'), files))

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

line_CHAM_26_1 = go.Scatter(x=dataset_CHAM_26_1['Cycle'],
                            y=dataset_CHAM_26_1['AH-OUT-NOMINAL'],
                            name='CHAM_26_1',
                            marker_color='rgb(255,0,0)')

line_CHAM_26_2 = go.Scatter(x=dataset_CHAM_26_2['Cycle'],
                            y=dataset_CHAM_26_2['AH-OUT-NOMINAL'],
                            name='CHAM_26_2',
                            marker_color='rgb(255,0,0)',
                            line=dict(dash='dash'))

# ====================CHAM_32====================
CHAM_32_path = 'Cycle_Data/CHAM_32/'
files = os.listdir(CHAM_32_path)

CHAM_32_1_files = list(
    filter(lambda x: (x[0:9] == 'CHAM_32_1' and x[-4:] == '.csv'), files))
CHAM_32_2_files = list(
    filter(lambda x: (x[0:9] == 'CHAM_32_2' and x[-4:] == '.csv'), files))

CHAM_32_1_list = []
for file in CHAM_32_1_files:
    tmp = pd.read_csv(CHAM_32_path + file, header=8)
    CHAM_32_1_list.append(tmp)
CHAM_32_1_list = sorted(CHAM_32_1_list, key=lambda k: k['Date'][0])

CHAM_32_2_list = []
for file in CHAM_32_2_files:
    tmp = pd.read_csv(CHAM_32_path + file, header=8)
    CHAM_32_2_list.append(tmp)
CHAM_32_2_list = sorted(CHAM_32_2_list, key=lambda k: k['Date'][0])

dataset_CHAM_32_1 = pd.concat(
    CHAM_32_1_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_CHAM_32_1)):
    dataset_CHAM_32_1.loc[data, 'Cycle'] = data

dataset_CHAM_32_1['AH-OUT-NOMINAL'] = dataset_CHAM_32_1.apply(
    lambda x: x['AH-OUT'] / dataset_CHAM_32_1.loc[0, 'AH-OUT'], axis=1)

dataset_CHAM_32_2 = pd.concat(
    CHAM_32_2_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_CHAM_32_2)):
    dataset_CHAM_32_2.loc[data, 'Cycle'] = data

dataset_CHAM_32_2['AH-OUT-NOMINAL'] = dataset_CHAM_32_2.apply(
    lambda x: x['AH-OUT'] / dataset_CHAM_32_2.loc[0, 'AH-OUT'], axis=1)

line_CHAM_32_1 = go.Scatter(x=dataset_CHAM_32_1['Cycle'],
                            y=dataset_CHAM_32_1['AH-OUT-NOMINAL'],
                            name='CHAM_32_1',
                            marker_color='rgb(0,255,0)')

line_CHAM_32_2 = go.Scatter(x=dataset_CHAM_32_2['Cycle'],
                            y=dataset_CHAM_32_2['AH-OUT-NOMINAL'],
                            name='CHAM_32_2',
                            marker_color='rgb(0,255,0)',
                            line=dict(dash='dash'))

# ====================MOLI_28====================
MOLI_28_path = 'Cycle_Data/MOLI_28/'
files = os.listdir(MOLI_28_path)

MOLI_28_1_files = list(
    filter(lambda x: (x[0:9] == 'MOLI_28_1' and x[-4:] == '.csv'), files))
MOLI_28_2_files = list(
    filter(lambda x: (x[0:9] == 'MOLI_28_2' and x[-4:] == '.csv'), files))

MOLI_28_1_list = []
for file in MOLI_28_1_files:
    tmp = pd.read_csv(MOLI_28_path + file, header=8)
    MOLI_28_1_list.append(tmp)
MOLI_28_1_list = sorted(MOLI_28_1_list, key=lambda k: k['Date'][0])

MOLI_28_2_list = []
for file in MOLI_28_2_files:
    tmp = pd.read_csv(MOLI_28_path + file, header=8)
    MOLI_28_2_list.append(tmp)
MOLI_28_2_list = sorted(MOLI_28_2_list, key=lambda k: k['Date'][0])

dataset_MOLI_28_1 = pd.concat(
    MOLI_28_1_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_MOLI_28_1)):
    dataset_MOLI_28_1.loc[data, 'Cycle'] = data

dataset_MOLI_28_1['AH-OUT-NOMINAL'] = dataset_MOLI_28_1.apply(
    lambda x: x['AH-OUT'] / dataset_MOLI_28_1.loc[0, 'AH-OUT'], axis=1)

dataset_MOLI_28_2 = pd.concat(
    MOLI_28_2_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_MOLI_28_2)):
    dataset_MOLI_28_2.loc[data, 'Cycle'] = data

dataset_MOLI_28_2['AH-OUT-NOMINAL'] = dataset_MOLI_28_2.apply(
    lambda x: x['AH-OUT'] / dataset_MOLI_28_2.loc[0, 'AH-OUT'], axis=1)

line_MOLI_28_1 = go.Scatter(x=dataset_MOLI_28_1['Cycle'],
                            y=dataset_MOLI_28_1['AH-OUT-NOMINAL'],
                            name='MOLI_28_1',
                            marker_color='rgb(0,0,255)')

line_MOLI_28_2 = go.Scatter(x=dataset_MOLI_28_2['Cycle'],
                            y=dataset_MOLI_28_2['AH-OUT-NOMINAL'],
                            name='MOLI_28_2',
                            marker_color='rgb(0,0,255)',
                            line=dict(dash='dash'))

# ====================MOLI_42====================
MOLI_42_path = 'Cycle_Data/MOLI_42/'
files = os.listdir(MOLI_42_path)

MOLI_42_1_files = list(
    filter(lambda x: (x[0:9] == 'MOLI_42_1' and x[-4:] == '.csv'), files))
MOLI_42_2_files = list(
    filter(lambda x: (x[0:9] == 'MOLI_42_2' and x[-4:] == '.csv'), files))

MOLI_42_1_list = []
for file in MOLI_42_1_files:
    tmp = pd.read_csv(MOLI_42_path + file, header=8)
    MOLI_42_1_list.append(tmp)
MOLI_42_1_list = sorted(MOLI_42_1_list, key=lambda k: k['Date'][0])

MOLI_42_2_list = []
for file in MOLI_42_2_files:
    tmp = pd.read_csv(MOLI_42_path + file, header=8)
    MOLI_42_2_list.append(tmp)
MOLI_42_2_list = sorted(MOLI_42_2_list, key=lambda k: k['Date'][0])

dataset_MOLI_42_1 = pd.concat(
    MOLI_42_1_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_MOLI_42_1)):
    dataset_MOLI_42_1.loc[data, 'Cycle'] = data

dataset_MOLI_42_1['AH-OUT-NOMINAL'] = dataset_MOLI_42_1.apply(
    lambda x: x['AH-OUT'] / dataset_MOLI_42_1.loc[0, 'AH-OUT'], axis=1)

dataset_MOLI_42_2 = pd.concat(
    MOLI_42_2_list, axis=0, join='outer', ignore_index=True)
for data in range(len(dataset_MOLI_42_2)):
    dataset_MOLI_42_2.loc[data, 'Cycle'] = data

dataset_MOLI_42_2['AH-OUT-NOMINAL'] = dataset_MOLI_42_2.apply(
    lambda x: x['AH-OUT'] / dataset_MOLI_42_2.loc[0, 'AH-OUT'], axis=1)

line_MOLI_42_1 = go.Scatter(x=dataset_MOLI_42_1['Cycle'],
                            y=dataset_MOLI_42_1['AH-OUT-NOMINAL'],
                            name='MOLI_42_1',
                            marker_color='rgb(255,255,0)')

line_MOLI_42_2 = go.Scatter(x=dataset_MOLI_42_2['Cycle'],
                            y=dataset_MOLI_42_2['AH-OUT-NOMINAL'],
                            name='MOLI_42_2',
                            marker_color='rgb(255,255,0)',
                            line=dict(dash='dash'))

# ====================Plot codes====================
fig = go.Figure([line_CHAM_26_1,
                 line_CHAM_26_2,

                 line_CHAM_32_1,
                 line_CHAM_32_2,

                 line_MOLI_28_1,
                 line_MOLI_28_2,

                 line_MOLI_42_1,
                 line_MOLI_42_2
                 ])

fig.update_layout(
    title='Battery AH-OUT-NOMINAL/Cycle Data',
    xaxis_title='Cycle',
    yaxis_title='AH-OUT-NOMINAL',
    hovermode='x'
)

fig.show()
