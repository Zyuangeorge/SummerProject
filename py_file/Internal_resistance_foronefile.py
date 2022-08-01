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

    internal_resistance_1 = (point2.iat[0,7] - point1.iat[0,7]) / (point2.iat[0,6] - point1.iat[0,6])
    internal_resistance_2 = (point4.iat[0,7] - point3.iat[0,7]) / (point4.iat[0,6] - point3.iat[0,6])

    output_resistance = pd.DataFrame([[cycle, internal_resistance_1, internal_resistance_2]], columns=[
                                     'Cycle', 'Internal_resistance_1', 'Internal_resistance_2'])

    return output_resistance


def create_resistance_lines(data):
    df = data
    full_cycle_number = df['Cyc#'].max()

    output_fullcycle = pd.DataFrame(
        columns=['Cycle', 'Internal_resistance_1', 'Internal_resistance_2'])

    for i in range(full_cycle_number - 1):
        calculated_data = get_resistance_per_cycle(df, i + 1)

        output_fullcycle = pd.concat(
            [output_fullcycle, calculated_data], ignore_index=True)

    internal_resistance_curve_1 = go.Scatter(x=output_fullcycle['Cycle'],
                                             y=output_fullcycle['Internal_resistance_1'],
                                             name='Internal resistance_1')

    internal_resistance_curve_2 = go.Scatter(x=output_fullcycle['Cycle'],
                                             y=output_fullcycle['Internal_resistance_2'],
                                             name='Internal resistance_2')

    return [internal_resistance_curve_1, internal_resistance_curve_2]


def plot_curves(root_path):
    '''Plot curves based on the root folder'''
    original_data = pd.read_csv(root_path, header=1)
    curve_1, curve_2 = create_resistance_lines(original_data)

    # Plot the lines
    fig = go.Figure([curve_1, curve_2])

    # Set the graph layout
    fig.update_layout(
        title='Battery Internal resistance/Cycle Data',
        xaxis_title='Cycle',
        yaxis_title='Internal resistance (R)',
        hovermode='x'
    )

    return fig


# ====================MAIN====================
if __name__ == "__main__":

    #fig = plot_curves('Cycle_Data_2/ZW_CHAM_M_2000cycles_1.csv')
    fig = plot_curves('Cycle_Data_2/ZW_Cham200cycles_1C_repeat.013.csv')

    fig.show()
