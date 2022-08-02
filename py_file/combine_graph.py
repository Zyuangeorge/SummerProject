import os
import datetime
import pandas as pd
import plotly.graph_objects as go


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

    # Create a new series called efficiency
    capacitance_efficiency_data['EFFICIENCY'] = capacitance_efficiency_data.apply(
        lambda x: x['WH-OUT'] / x['WH-IN'], axis=1)

    return capacitance_efficiency_data


def calculate_nominal_resistance(data):
    resistance_data = data

    resistance_data['Internal_resistance_1_nominal'] = resistance_data.apply(
        lambda x: x['Internal_resistance_1'] / resistance_data.loc[0, 'Internal_resistance_1'], axis=1)

    resistance_data['Internal_resistance_2_nominal'] = resistance_data.apply(
        lambda x: x['Internal_resistance_2'] / resistance_data.loc[0, 'Internal_resistance_2'], axis=1)

    return resistance_data


def create_lines(battery_data_set_for_resistance, battery_data_set_for_efficiency_capacitance, battery_name):

    internal_resistance_data_full_cycle = []

    # Create internal resistance data
    for data in battery_data_set_for_resistance:
        internal_resistance_data = calculate_internal_resistance(data)
        internal_resistance_data_full_cycle.append(internal_resistance_data)

    internal_resistance_data_full_cycle = pd.concat(
        internal_resistance_data_full_cycle, axis=0, join='outer', ignore_index=True)

    internal_resistance_data_full_cycle = calculate_nominal_resistance(
        internal_resistance_data_full_cycle)

    # Create efficiency and capacitance data
    efficiency__capacitance_data_full_cycle = calculate_capacitance_efficiency(
        battery_data_set_for_efficiency_capacitance)

    # Reset Cyc# value
    internal_resistance_data_full_cycle['Cyc#'] = list(
        internal_resistance_data_full_cycle.index)

    # Create 4 kinds of lines
    line__resistance_1 = go.Scatter(x=internal_resistance_data_full_cycle['Cyc#'],
                                    y=internal_resistance_data_full_cycle['Internal_resistance_1_nominal'],
                                    name=battery_name + '_' + 'Internal resistance_1')

    line__resistance_2 = go.Scatter(x=internal_resistance_data_full_cycle['Cyc#'],
                                    y=internal_resistance_data_full_cycle['Internal_resistance_2_nominal'],
                                    name=battery_name + '_' + 'Internal resistance_2')

    line_capacitance = go.Scatter(x=efficiency__capacitance_data_full_cycle['Cycle'],
                                  y=efficiency__capacitance_data_full_cycle['AH-OUT-NOMINAL'],
                                  name=battery_name + '_' + 'Capacitance')

    line_efficiency = go.Scatter(x=efficiency__capacitance_data_full_cycle['Cycle'],
                                 y=efficiency__capacitance_data_full_cycle['EFFICIENCY'],
                                 name=battery_name + '_' + 'Efficiency')

    return line__resistance_1, line__resistance_2, line_capacitance, line_efficiency


def convert_to_timestamp(dateStr):
    return datetime.datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S").timestamp()


def create_dataset_for_resistance(folder_path):
    # File list
    file_list = os.listdir(folder_path)
    battery_1_data = []
    battery_2_data = []

    folder_name = folder_path

    # Filter out other files
    battery_1_file_namelist = list(
        filter(lambda x: (x[7:10] == '_1_' and x[-4:] == '.csv'), file_list))
    battery_2_file_namelist = list(
        filter(lambda x: (x[7:10] == '_2_' and x[-4:] == '.csv'), file_list))

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

    return battery_1_data, battery_2_data


def create_dataset_for_efficiency_and_capacitance(folder_path):
    # File list
    file_list = os.listdir(folder_path)
    battery_1_data = []
    battery_2_data = []

    folder_name = folder_path

    # Filter out other files
    battery_1_file_namelist = list(
        filter(lambda x: (x[7:10] == '_1_' and x[-4:] == '.csv'), file_list))
    battery_2_file_namelist = list(
        filter(lambda x: (x[7:10] == '_2_' and x[-4:] == '.csv'), file_list))

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
    battery_1_data = pd.concat(
        battery_1_data, axis=0, join='outer', ignore_index=True)

    battery_2_data = pd.concat(
        battery_2_data, axis=0, join='outer', ignore_index=True)

    battery_1_data['Cycle'] = list(battery_1_data.index)
    battery_2_data['Cycle'] = list(battery_2_data.index)

    return battery_1_data, battery_2_data


def plot_graph(folder_path_resistance, folder_path_eff_cap):

    folder_name = folder_path_resistance

    battery_data_resistance_1, battery_data_resistance_2 = create_dataset_for_resistance(
        folder_path_resistance)
    battery_data_eff_cap_1, battery_data_eff_cap_2 = create_dataset_for_efficiency_and_capacitance(
        folder_path_eff_cap)

    battery_1_line_1, battery_1_line_2, battery_1_line_3, battery_1_line_4 = create_lines(
        battery_data_resistance_1, battery_data_eff_cap_1, folder_name[15:22])
    battery_2_line_1, battery_2_line_2, battery_2_line_3, battery_2_line_4 = create_lines(
        battery_data_resistance_2, battery_data_eff_cap_2, folder_name[15:22] + '_2')

    fig = go.Figure([battery_1_line_1, battery_1_line_2, battery_1_line_3, battery_1_line_4,
                     battery_2_line_1, battery_2_line_2, battery_2_line_3, battery_2_line_4])

    fig.update_layout(
        title='Battery Characteristics/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='Nominal value',
        hovermode='x unified',
        yaxis_range=[0.5, 1.2]
    )

    fig.show()


# ====================MAIN====================
if __name__ == "__main__":

    plot_graph('Full_Test_Data/MOLI_28/', 'Cycle_Data/MOLI_28/')
