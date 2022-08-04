import os
import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def calculate_internal_resistance(data):
    df = data  # input data

    cycle_number = df["Cyc#"].max()  # maximum cycle value

    output_data = pd.DataFrame(columns=[
                               'Cyc#', 'Internal_resistance_1', 'Internal_resistance_2'])  # output in dataframe

    for cycle in range(cycle_number - 1):
        # filter out the Amps > 0
        data_filtered = df.loc[(df['Cyc#'] == cycle + 1) & (df['Amps'] == 0)]

        # four points
        # point_1 and point_2 is at the negative current pulse
        # point_3 and point_4 is at the positive current pulse
        point_1 = data_filtered.head(1)
        point_1_amp = point_1.Amps[point_1.index].item()
        point_1_volts = point_1.Volts[point_1.index].item()

        point_2 = df[list(point_1.index)[0]-1:list(point_1.index)[0]]
        point_2_amp = point_2.Amps[point_2.index].item()
        point_2_volts = point_2.Volts[point_2.index].item()

        point_3 = data_filtered.tail(1)
        point_3_amp = point_3.Amps[point_3.index].item()
        point_3_volts = point_3.Volts[point_3.index].item()

        point_4 = df[list(point_3.index)[0]+1:list(point_3.index)[0]+2]
        point_4_amp = point_4.Amps[point_4.index].item()
        point_4_volts = point_4.Volts[point_4.index].item()

        # calculate internal resistance at negative and positive impulse
        internal_resistance_1 = (
            (point_1_volts - point_2_volts)/(point_1_amp - point_2_amp))
        internal_resistance_2 = (
            (point_4_volts - point_3_volts)/(point_4_amp - point_3_amp))

        output_data.loc[cycle] = [
            cycle, internal_resistance_1, internal_resistance_2]

    return output_data


def calculate_capacitance_efficiency(data):
    capacitance_efficiency_data = data

    # Create a new series called AH-OUT-NOMINAL
    capacitance_efficiency_data['AH-OUT-NOMINAL'] = capacitance_efficiency_data.apply(
        lambda x: x['AH-OUT'] / data.loc[0, 'AH-OUT'], axis=1)

    # Create a new series called Efficiency
    capacitance_efficiency_data['Efficiency'] = capacitance_efficiency_data.apply(
        lambda x: x['WH-OUT'] / x['WH-IN'], axis=1)

    return capacitance_efficiency_data


def calculate_nominal_resistance(data):
    resistance_data = data

    resistance_data['Internal_resistance_1_nominal'] = resistance_data.apply(
        lambda x: x['Internal_resistance_1'] / resistance_data.loc[0, 'Internal_resistance_1'], axis=1)

    resistance_data['Internal_resistance_2_nominal'] = resistance_data.apply(
        lambda x: x['Internal_resistance_2'] / resistance_data.loc[0, 'Internal_resistance_2'], axis=1)

    return resistance_data


def convert_to_timestamp(dateStr):
    return datetime.datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S").timestamp()


def combine_internal_resistance_data(battery_data):
    internal_resistance_data_full_cycle = []

    # Create internal resistance data
    for data in battery_data:
        internal_resistance_data = calculate_internal_resistance(data)
        internal_resistance_data_full_cycle.append(internal_resistance_data)

    internal_resistance_data_full_cycle = pd.concat(
        internal_resistance_data_full_cycle, axis=0, join='outer', ignore_index=True)

    # Reset Cyc# value
    internal_resistance_data_full_cycle['Cyc#'] = list(
        internal_resistance_data_full_cycle.index)

    return internal_resistance_data_full_cycle


def combine_eff_cap_data(battery_data):
    # Merge the data in the list to one dataframe variable
    battery_data = pd.concat(
        battery_data, axis=0, join='outer', ignore_index=True)

    battery_data['Cycle'] = list(battery_data.index)

    return battery_data


def get_file_name_list(folder_name, file_list):

    if folder_name[-7:] == 'DLG_30/':
        # Filter for DLG_30
        battery_1_file_namelist = list(
            filter(lambda x: (x[6:9] == '_1_' and x[-4:] == '.csv'), file_list))
        battery_2_file_namelist = list(
            filter(lambda x: (x[6:9] == '_2_' and x[-4:] == '.csv'), file_list))
    elif folder_name[-9:] == 'DMEGC_26/':
        # Filter for DMEGC_26
        battery_1_file_namelist = list(
            filter(lambda x: (x[8:11] == '_1_' and x[-4:] == '.csv'), file_list))
        battery_2_file_namelist = list(
            filter(lambda x: (x[8:11] == '_2_' and x[-4:] == '.csv'), file_list))
    else:
        # Filter out other files
        battery_1_file_namelist = list(
            filter(lambda x: (x[7:10] == '_1_' and x[-4:] == '.csv'), file_list))
        battery_2_file_namelist = list(
            filter(lambda x: (x[7:10] == '_2_' and x[-4:] == '.csv'), file_list))

    return battery_1_file_namelist, battery_2_file_namelist


def create_dataset_for_resistance(folder_path):
    # File list
    file_list = os.listdir(folder_path)
    battery_1_data = []
    battery_2_data = []

    folder_name = folder_path

    battery_1_file_namelist, battery_2_file_namelist = get_file_name_list(
        folder_name, file_list)

    # Read the file in the file list
    for file_name in battery_1_file_namelist:
        tmp = pd.read_csv(folder_name + file_name, header=2)
        battery_1_data.append(tmp)

    for file_name in battery_2_file_namelist:
        tmp = pd.read_csv(folder_name + file_name, header=2)
        battery_2_data.append(tmp)

    # Sort the list based on the time information
    battery_1_data = sorted(
        battery_1_data, key=lambda date: convert_to_timestamp(date['DPt Time'][0]))
    battery_2_data = sorted(
        battery_2_data, key=lambda date: convert_to_timestamp(date['DPt Time'][0]))

    battery_1_data = combine_internal_resistance_data(battery_1_data)
    battery_2_data = combine_internal_resistance_data(battery_2_data)

    # Create nominal resistance data
    internal_resistance_data__1 = calculate_nominal_resistance(
        battery_1_data)
    internal_resistance_data__2 = calculate_nominal_resistance(
        battery_2_data)

    return internal_resistance_data__1, internal_resistance_data__2


def create_dataset_for_efficiency_and_capacitance(folder_path):
    # File list
    file_list = os.listdir(folder_path)
    battery_1_data = []
    battery_2_data = []

    folder_name = folder_path

    battery_1_file_namelist, battery_2_file_namelist = get_file_name_list(
        folder_name, file_list)

    # Read the file in the file list
    for file_name in battery_1_file_namelist:
        tmp = pd.read_csv(folder_name + file_name, header=8)
        battery_1_data.append(tmp)

    for file_name in battery_2_file_namelist:
        tmp = pd.read_csv(folder_name + file_name, header=8)
        battery_2_data.append(tmp)

    # Sort the list based on the time information
    battery_1_data = sorted(battery_1_data, key=lambda k: k['Date'][0])
    battery_2_data = sorted(battery_2_data, key=lambda k: k['Date'][0])

    # Merge the data in the list to one dataframe variable
    battery_1_data = combine_eff_cap_data(battery_1_data)
    battery_2_data = combine_eff_cap_data(battery_2_data)

    # Create efficiency and capacitance data
    efficiency__capacitance_data_1 = calculate_capacitance_efficiency(
        battery_1_data)
    efficiency__capacitance_data_2 = calculate_capacitance_efficiency(
        battery_2_data)

    return efficiency__capacitance_data_1, efficiency__capacitance_data_2


def create_lines(battery_data_set_for_resistance, battery_data_set_for_efficiency_capacitance, battery_name):

    internal_resistance_data_full_cycle = battery_data_set_for_resistance
    efficiency__capacitance_data_full_cycle = battery_data_set_for_efficiency_capacitance

    # Create 4 kinds of lines
    line__resistance_1 = go.Scatter(x=internal_resistance_data_full_cycle['Cyc#'],
                                    y=internal_resistance_data_full_cycle['Internal_resistance_1_nominal'],
                                    name=battery_name + '_' + 'Internal resistance_1')

    line__resistance_2 = go.Scatter(x=internal_resistance_data_full_cycle['Cyc#'],
                                    y=internal_resistance_data_full_cycle['Internal_resistance_2_nominal'],
                                    name=battery_name + '_' + 'Internal resistance_2')

    line_capacitance = go.Scatter(x=efficiency__capacitance_data_full_cycle['Cycle'],
                                  y=efficiency__capacitance_data_full_cycle['AH-OUT-NOMINAL'],
                                  name=battery_name + '_' + 'Capacity')

    line_efficiency = go.Scatter(x=efficiency__capacitance_data_full_cycle['Cycle'],
                                 y=efficiency__capacitance_data_full_cycle['Efficiency'],
                                 name=battery_name + '_' + 'Efficiency')

    return line__resistance_1, line__resistance_2, line_capacitance, line_efficiency


def combine_dataset(battery_data_resistance, battery_data_eff_cap, battery_name):

    resistance_data = pd.DataFrame(battery_data_resistance, columns=[
                                   'Internal_resistance_1_nominal', 'Internal_resistance_2_nominal'])
    eff_cap_data = pd.DataFrame(battery_data_eff_cap, columns=[
                                'Cycle', 'AH-OUT-NOMINAL', 'Efficiency'])
    eff_cap_data = eff_cap_data.rename(columns={'AH-OUT-NOMINAL': 'Capacity'})

    combined_data = pd.concat(
        [eff_cap_data, resistance_data], axis=1)

    output_data = pd.melt(combined_data, id_vars='Cycle',
                          var_name='Data_type', value_name='Nominal Value')

    output_data['Battery_name'] = battery_name

    return output_data


def plot_graph_go(folder_path_resistance, folder_path_eff_cap):

    folder_name = folder_path_resistance
    if folder_name[-7:] == 'DLG_30/':
        line_name = 'DLG_30'
    elif folder_name[-9:] == 'DMEGC_26/':
        line_name = 'DMEGC_26'
    else:
        line_name = folder_name[15:22]

    battery_data_resistance_1, battery_data_resistance_2 = create_dataset_for_resistance(
        folder_path_resistance)
    battery_data_eff_cap_1, battery_data_eff_cap_2 = create_dataset_for_efficiency_and_capacitance(
        folder_path_eff_cap)

    battery_1_line_1, battery_1_line_2, battery_1_line_3, battery_1_line_4 = create_lines(
        battery_data_resistance_1, battery_data_eff_cap_1, line_name + '_1')
    battery_2_line_1, battery_2_line_2, battery_2_line_3, battery_2_line_4 = create_lines(
        battery_data_resistance_2, battery_data_eff_cap_2, line_name + '_2')

    fig = go.Figure([battery_1_line_1, battery_1_line_2, battery_1_line_3, battery_1_line_4,
                     battery_2_line_1, battery_2_line_2, battery_2_line_3, battery_2_line_4])

    fig.update_layout(
        title='Battery Characteristics/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='Nominal value',
        hovermode='x',
        yaxis_range=[0.5, 1.2]
    )

    return fig


def plot_graph_px(folder_path_resistance, folder_path_eff_cap):

    folder_name = folder_path_resistance
    if folder_name[-7:] == 'DLG_30/':
        battery_name = 'DLG_30'
    elif folder_name[-9:] == 'DMEGC_26/':
        battery_name = 'DMEGC_26'
    else:
        battery_name = folder_name[15:22]

    battery_data_resistance_1, battery_data_resistance_2 = create_dataset_for_resistance(
        folder_path_resistance)
    battery_data_eff_cap_1, battery_data_eff_cap_2 = create_dataset_for_efficiency_and_capacitance(
        folder_path_eff_cap)

    battery_data_1 = combine_dataset(
        battery_data_resistance_1, battery_data_eff_cap_1, battery_name + '_1')
    battery_data_2 = combine_dataset(
        battery_data_resistance_2, battery_data_eff_cap_2, battery_name + '_2')

    final_data = pd.concat([battery_data_1, battery_data_2], ignore_index=True)

    fig = px.scatter(final_data, x='Cycle', y='Nominal Value',
                     color='Data_type', title='Nominal Value/Cycle Curves', trendline='lowess', symbol='Battery_name', category_orders={'Battery_name': [battery_name + '_1', battery_name + '_2']})

    fig.data = [t for t in fig.data if t.mode == 'lines']

    # fig.update_layout(yaxis_range=[0.5, 1.2])
    fig.update_traces(showlegend=True)

    return fig


# ====================MAIN====================
if __name__ == "__main__":

    # fig = plot_graph_go('Full_Test_Data/DMEGC_26/', 'Cycle_Data/DMEGC_26/')
    # fig = plot_graph_go('Full_Test_Data/DMEGC_26/', 'Cycle_Data/DMEGC_26/')
    # fig = plot_graph_px('Full_Test_Data/DLG_30/', 'Cycle_Data/DLG_30/')
    fig = plot_graph_px('Full_Test_Data/DMEGC_26/', 'Cycle_Data/DMEGC_26/')

    fig.show()
