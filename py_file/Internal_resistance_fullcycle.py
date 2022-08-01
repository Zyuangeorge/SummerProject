import os
import functools
import operator
import random
import time
import datetime
import pandas as pd
import plotly.graph_objects as go


def get_resistance_per_cycle(data, cycle_number):
    df = data
    cycle = cycle_number

    battery1_1_filtered = df.loc[(df['Cyc#'] == cycle) & (
        df['Amps'] == 0)]  # when amp = 0

    point2 = battery1_1_filtered.head(1)
    point3 = battery1_1_filtered.tail(1)
    point1 = df[list(point2.index)[0]-1:list(point2.index)[0]]
    point4 = df[list(point3.index)[0]+1:list(point3.index)[0]+2]

    internal_resistance_1 = (
        point2.iat[0, 8] - point1.iat[0, 8]) / (point2.iat[0, 7] - point1.iat[0, 7])
    internal_resistance_2 = (
        point4.iat[0, 8] - point3.iat[0, 8]) / (point4.iat[0, 7] - point3.iat[0, 7])

    output_resistance = pd.DataFrame([[cycle, internal_resistance_1, internal_resistance_2]], columns=[
                                     'Cyc#', 'Internal_resistance_1', 'Internal_resistance_2'])

    return output_resistance


def get_fullcycle_resistance(data):
    df = data
    full_cycle_number = df['Cyc#'].max()

    output_fullcycle = pd.DataFrame(
        columns=['Cyc#', 'Internal_resistance_1', 'Internal_resistance_2'])

    for i in range(full_cycle_number - 1):
        calculated_data = get_resistance_per_cycle(df, i + 1)

        output_fullcycle = pd.concat(
            [output_fullcycle, calculated_data], ignore_index=True)

    return output_fullcycle


def convert_to_timestamp(dateStr):
    datetimeObj = datetime.datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
    timeStamp = int(time.mktime(datetimeObj.timetuple()))
    return timeStamp


def create_lines(file_path):
    '''Plot the internal resistance for full cycle'''
    # File lists
    battery1_file_list = []
    battery2_file_list = []

    battery1_file_sorted = []
    battery2_file_sorted = []

    line_list = []

    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    line_name = file_path[14:21]

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
        tmp = pd.read_csv(folder_name + file, header=2)
        battery1_file_sorted.append(tmp)

    for file in battery2_file_list:
        tmp = pd.read_csv(folder_name + file, header=2)
        battery2_file_sorted.append(tmp)

    """ # Reset the DPt Time values
    for file in battery1_file_sorted:
        for data in range(len(file)):
            file.loc[data, 'DPt Time'] = convert_to_timestamp(
                file.loc[data, 'DPt Time'])

    for file in battery2_file_sorted:
        for data in range(len(file)):
            file.loc[data, 'DPt Time'] = convert_to_timestamp(
                file.loc[data, 'DPt Time'])

    print(battery1_file_sorted, battery2_file_sorted) """

    battery1_file_sorted = sorted(
        battery1_file_sorted, key=lambda k: k['DPt Time'][0])
    battery2_file_sorted = sorted(
        battery2_file_sorted, key=lambda k: k['DPt Time'][0])

    # Merge the data in the list to one dataframe variable
    dataset_battery1 = pd.concat(
        battery1_file_sorted, axis=0, join='outer', ignore_index=True)

    dataset_battery2 = pd.concat(
        battery2_file_sorted, axis=0, join='outer', ignore_index=True)

    # Reset the cycle values
    for data in range(len(dataset_battery1)):
        dataset_battery1.loc[data, 'Cyc#'] = data
    for data in range(len(dataset_battery2)):
        dataset_battery2.loc[data, 'Cyc#'] = data

    # Create a new series called internal resistance
    battery1_internal_resistance = get_fullcycle_resistance(dataset_battery1)
    battery2_internal_resistance = get_fullcycle_resistance(dataset_battery2)

    dataset_battery1 = pd.merge(
        dataset_battery1, battery1_internal_resistance, how='outer', on='Cyc#')
    dataset_battery2 = pd.merge(
        dataset_battery2, battery2_internal_resistance, how='outer', on='Cyc#')

    # Plot the curves
    line_battery1_internal_resistance_1 = go.Scatter(x=dataset_battery1['Cyc#'],
                                                     y=dataset_battery1['Internal_resistance_1'],
                                                     name=line_name + '_1' + '_IR_1',
                                                     marker_color=color)

    line_battery1_internal_resistance_2 = go.Scatter(x=dataset_battery1['Cyc#'],
                                                     y=dataset_battery1['Internal_resistance_2'],
                                                     name=line_name + '_1' + '_IR_2',
                                                     marker_color=color)

    line_battery2_internal_resistance_1 = go.Scatter(x=dataset_battery2['Cyc#'],
                                                     y=dataset_battery2['Internal_resistance_1'],
                                                     name=line_name + '_2' + '_IR_1',
                                                     marker_color=color,
                                                     line=dict(dash='dash'))

    line_battery2_internal_resistance_2 = go.Scatter(x=dataset_battery2['Cyc#'],
                                                     y=dataset_battery2['Internal_resistance_2'],
                                                     name=line_name + '_2' + '_IR_2',
                                                     marker_color=color,
                                                     line=dict(dash='dash'))

    line_list = [
        line_battery1_internal_resistance_1,
        line_battery1_internal_resistance_2,
        line_battery2_internal_resistance_1,
        line_battery2_internal_resistance_2]

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
        title='Battery internal resistance/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='internal resistance (R)',
        hovermode='x'
    )

    return fig


# ====================MAIN====================
if __name__ == "__main__":

    fig = plot_curves('Full_Test_Data/')

    fig.show()
