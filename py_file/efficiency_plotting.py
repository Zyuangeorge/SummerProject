import os
import functools
import operator
import random
import pandas as pd
import plotly.graph_objects as go

def create_lines(file_path):
    '''Plot the nominal curve, file structure should be folder-scv'''
    # File lists
    battery1_file_list = []
    battery2_file_list = []

    battery1_file_sorted = []
    battery2_file_sorted = []
    
    line_list = []
    
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    
    line_name = file_path[11:18]
    
    # Set the file list of the folder
    folder_name = file_path

    file_list = os.listdir(file_path)

    # Filter out other files
    battery1_file_list = list(
        filter(lambda x: (x[7:10] == '_1_' and x[-4:] == '.csv'), file_list))
    battery2_file_list = list(
        filter(lambda x: (x[7:10] == '_2_' and x[-4:] == '.csv'), file_list))
    
    # Read the file in the file list and sort the list based on the time information
    for file in battery1_file_list:
        tmp = pd.read_csv(folder_name + file, header=8)
        battery1_file_sorted.append(tmp)

    for file in battery2_file_list:
        tmp = pd.read_csv(folder_name + file, header=8)
        battery2_file_sorted.append(tmp)

    battery1_file_sorted = sorted(battery1_file_sorted, key=lambda k: k['Date'][0])
    battery2_file_sorted = sorted(battery2_file_sorted, key=lambda k: k['Date'][0])

    # Merge the data in the list to one dataframe variable
    dataset_battery1 = pd.concat(
        battery1_file_sorted, axis=0, join='outer', ignore_index=True)

    dataset_battery2 = pd.concat(
        battery2_file_sorted, axis=0, join='outer', ignore_index=True)

    # Reset the cycle values
    for data in range(len(dataset_battery1)):
        dataset_battery1.loc[data, 'Cycle'] = data
    for data in range(len(dataset_battery2)):
        dataset_battery2.loc[data, 'Cycle'] = data
    
    # Create a new series called efficiency
    dataset_battery1['EFFICIENCY'] = dataset_battery1.apply(
        lambda x: x['WH-OUT'] / x['WH-IN'] * 100, axis=1)
    
    dataset_battery2['EFFICIENCY'] = dataset_battery2.apply(
        lambda x: x['WH-OUT'] / x['WH-IN'] * 100, axis=1)
    
    dataset_battery1['TYPE'] = line_name
    dataset_battery2['TYPE'] = line_name
    
    # Plot the curves
    line_battery1 = go.Scatter(x=dataset_battery1['Cycle'],
                                y=dataset_battery1['EFFICIENCY'],
                                name= line_name + '_1',
                                marker_color = color)

    line_battery2 = go.Scatter(x=dataset_battery2['Cycle'],
                                y=dataset_battery2['EFFICIENCY'],
                                name= line_name + '_2',
                                marker_color = color,
                                line=dict(dash='dash'))
    
    line_list = [line_battery1, line_battery2]
    
    return line_list

def plot_curves(root_path):
    '''Plot curves based on the root folder'''
    folder_list = []
    line_list = []
    lines = []
    
    # Create folder list
    folder_list = os.listdir(root_path)

    # Sort the folder list based on the folder names
    folder_list.sort()

    # Create line list
    for folder in folder_list:
        folder_name = root_path + folder + '/'
        line_list.append(create_lines(folder_name))

    # Transfer nested line list to flat line list
    lines = functools.reduce(operator.concat, line_list)

    # Plot the lines
    fig = go.Figure(lines)

    # Set the graph layout
    fig.update_layout(
        title='Battery EFFICIENCY/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='EFFICIENCY (%)',
        hovermode='x',
        yaxis_range = [80,100]
    )

    return fig

# ====================MAIN====================
if __name__ == "__main__":

    fig = plot_curves('Cycle_Data/')

    fig.show()
