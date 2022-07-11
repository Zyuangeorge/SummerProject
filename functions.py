import pandas as pd

def get_internal_resistance(data, cycle_number):
    df = data
    cycle = cycle_number

    battery1_1_filtered = df.loc[(df['Cyc#'] == cycle) & (df['Amps'] == 0)] # when amp = 0

    point2 = battery1_1_filtered.head(1)
    point3 = battery1_1_filtered.tail(1)
    point1 = df[list(point2.index)[0]-1:list(point2.index)[0]]
    point4 = df[list(point3.index)[0]+1:list(point3.index)[0]+2]

    internal_resistance_1 = (point2.iat[0,8] - point1.iat[0,8]) / (point2.iat[0,7] - point1.iat[0,7])
    internal_resistance_2 = (point4.iat[0,8] - point3.iat[0,8]) / (point4.iat[0,7] - point3.iat[0,7])
    
    output = pd.DataFrame([[cycle, internal_resistance_1], [cycle, internal_resistance_2]], columns=['Cycle', 'Internal_resistance'])

    print(internal_resistance_1,internal_resistance_2)

    return output
