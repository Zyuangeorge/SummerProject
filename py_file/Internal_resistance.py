import pandas as pd
import plotly.graph_objects as go

def get_resistance_per_cycle(data, cycle_number):
    df = data
    cycle = cycle_number

    battery1_1_filtered = df.loc[(df['Cyc#'] == cycle) & (df['Amps'] == 0)] # when amp = 0

    point2 = battery1_1_filtered.head(1)
    point3 = battery1_1_filtered.tail(1)
    point1 = df[list(point2.index)[0]-1:list(point2.index)[0]]
    point4 = df[list(point3.index)[0]+1:list(point3.index)[0]+2]

    internal_resistance_1 = (point2.iat[0,7] - point1.iat[0,7]) / (point2.iat[0,6] - point1.iat[0,6])
    internal_resistance_2 = (point4.iat[0,7] - point3.iat[0,7]) / (point4.iat[0,6] - point3.iat[0,6])
    
    internal_resistance_total = (internal_resistance_1 + internal_resistance_2)/2
    output = pd.DataFrame([[cycle, internal_resistance_total]], columns=['Cycle', 'Internal_resistance'])
    #output = pd.DataFrame([[cycle, internal_resistance_1], [cycle, internal_resistance_2]], columns=['Cycle', 'Internal_resistance'])
    # output = {'Cycle':cycle, 'Internal_resistance':(internal_resistance_1 + internal_resistance_2)/2}
    return output

def get_resistance_data(data):
    df = data
    full_cycle = df['Cyc#'].max()

    output = pd.DataFrame(columns=['Cycle', 'Internal_resistance'])

    for i in range(full_cycle-1):
        calculated_data = get_resistance_per_cycle(df,i + 1)
        output = pd.concat([output, calculated_data], ignore_index = True)

    return output

def plot_curves(root_path):
    '''Plot curves based on the root folder'''
    original_data = pd.read_csv(root_path, header=1)
    data = get_resistance_data(original_data)

    internal_resistance_curve = go.Scatter( x=data['Cycle'],
                                            y=data['Internal_resistance'],
                                            name= 'Internal resistance')

    # Plot the lines
    fig = go.Figure(internal_resistance_curve)

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

    """ df=pd.read_csv('Cycle_Data_2/ZW_CHAM_M_2000cycles_1.csv', header=1)
    fig = get_resistance_data(df) 
    print(fig) """

    #fig = plot_curves('Cycle_Data_2/ZW_CHAM_M_2000cycles_1.csv')
    fig = plot_curves('Cycle_Data_2/ZW_Cham200cycles_1C_repeat.013.csv')
    
    fig.show()