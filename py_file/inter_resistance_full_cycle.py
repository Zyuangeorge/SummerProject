import os
import functools
import operator
import random
import time
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

def create_lines(file_path):
    csv_data = pd.read_csv(file_path, header = 1)

    internal_resistance_data = calculate_internal_resistance(csv_data)

    line_1 = go.Scatter(x=internal_resistance_data['Cyc#'],
                        y=internal_resistance_data['Internal_resistance_1'],
                        name='Internal resistance_1')

    line_2 = go.Scatter(x=internal_resistance_data['Cyc#'],
                        y=internal_resistance_data['Internal_resistance_2'],
                        name='Internal resistance_2')

    return line_1,line_2

def plot_graph(root_path):
    path = root_path

    line_1, line_2 = create_lines(path)

    fig = go.Figure([line_1,line_2])

    fig.update_layout(
        title='Battery Internal resistance/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='Internal resistance (R)',
        hovermode='x' 
    )
    
    return fig

def convert_to_timestamp(dateStr):
    datetimeObj = datetime.datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
    timeStamp = int(time.mktime(datetimeObj.timetuple()))
    return timeStamp

# ====================MAIN====================
if __name__ == "__main__":

    fig = plot_graph('Cycle_Data_2/ZW_Cham200cycles_1C_repeat.013.csv')

    fig.show()