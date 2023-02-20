import os
import datetime
import pandas as pd
import plotly.graph_objects as go

def calculate_internal_resistance(data):
    df = data # input data

    cycle_number = df["Cyc#"].max() # maximum cycle value

    output_data = pd.DataFrame(columns=['Cyc#','Internal_resistance_1','Internal_resistance_2']) # output in dataframe

    for cycle in range(cycle_number - 1):
        data_filtered = df.loc[(df['Cyc#'] == cycle + 1) & (df['Amps'] == 0)] # filter out the Amps > 0
        
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
        internal_resistance_1 = ((point_1_volts - point_2_volts)/(point_1_amp - point_2_amp))
        internal_resistance_2 = ((point_4_volts - point_3_volts)/(point_4_amp - point_3_amp))

        output_data.loc[cycle] = [cycle, internal_resistance_1, internal_resistance_2]
    
    return output_data

def create_lines(battery_data_set, battery_name):
    internal_resistance_data_full_cycle = []

    for data in battery_data_set:
        internal_resistance_data = calculate_internal_resistance(data)
        internal_resistance_data_full_cycle.append(internal_resistance_data)

    internal_resistance_data_full_cycle = pd.concat(
    internal_resistance_data_full_cycle, axis=0, join='outer', ignore_index=True)

    # Reset Cyc# value
    internal_resistance_data_full_cycle['Cyc#'] = list(internal_resistance_data_full_cycle.index)

    line_1 = go.Scatter(x=internal_resistance_data_full_cycle['Cyc#'],
                        y=internal_resistance_data_full_cycle['Internal_resistance_1'],
                        name=battery_name + '_' + 'Internal resistance_1')

    line_2 = go.Scatter(x=internal_resistance_data_full_cycle['Cyc#'],
                        y=internal_resistance_data_full_cycle['Internal_resistance_2'],
                        name=battery_name + '_' + 'Internal resistance_2')

    return line_1, line_2

def convert_to_timestamp(dateStr):
    return datetime.datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S").timestamp()

def create_dataset(folder_path):
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
    battery_1_data = sorted(battery_1_data, key = lambda date:convert_to_timestamp(date['DPt Time'][0]))
    battery_2_data = sorted(battery_2_data, key = lambda date:convert_to_timestamp(date['DPt Time'][0]))

    return battery_1_data, battery_2_data

def plot_graph(folder_path):
    folder_name = folder_path

    battery_data_1, battery_data_2 = create_dataset(folder_name)

    battery_1_line_1, battery_1_line_2 = create_lines(battery_data_1,folder_name[15:22])
    battery_2_line_1, battery_2_line_2 = create_lines(battery_data_2,folder_name[15:22] + '_2')

    fig = go.Figure([battery_1_line_1, battery_1_line_2,battery_2_line_1,battery_2_line_2])

    fig.update_layout(
        title='Battery Internal resistance/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='Internal resistance (R)',
        hovermode='x',
        yaxis_range = [-0.1,0.1]
    )
    
    fig.show()

# ====================MAIN====================
if __name__ == "__main__":
    plot_graph('Full_Test_Data/MOLI_42/')