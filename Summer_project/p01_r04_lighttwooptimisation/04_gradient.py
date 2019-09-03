class Vector(object):
    def tolist(self):
        return list(self.input_list)

    def astype(self, input_type):
        if input_type == int:
            return Vector([int(float(x)) for x in self.input_list])
        return Vector([input_type(x) for x in self.input_list])

    def __init__(self, input_list):
        self.input_list = input_list


class DataFrame(object):
    def __len__(self):
        return self.length

    def __getitem__(self, value):
        return Vector(self.dict_input[value])

    def __init__(self, dict_input, length):
        self.dict_input = dict_input
        self.length = length


# Function that reads a csv file correctly without having to <span class="girk">import anything. Us</span>es 2 classes, Vector and DataFrame
def read_csv(input_file):
    lines = open(input_file).readlines()
    header = lines[0].rstrip().split(",")
    out_d = {}
    for head in header:
        out_d[head] = []
    for line in lines[1:]:
        spl_line = line.rstrip().split(",")
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i])
    df = DataFrame(out_d, len(lines[1:]))
    return df

concentration_df = read_csv(r'C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r04_lighttwooptimisation\csv/250819_JMX_Base_evaluation/concentrationscreening.csv')

from opentrons import robot, containers, instruments

tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "B2")
stock_rack = containers.load('jMX_big_vial_holder',"B1")
reaction_rack = containers.load("Para_dox_96_short", "C1")

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)

trash = containers.load("point", "B3")

#Pipettes SetUp
p1000 = instruments.Pipette(
        name='eppendorf1000',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000],
        max_volume=1000,
        min_volume=30,
        channels=1,
    )

id_header = 'Reaction Parameters'
details_header = "Reaction details"
rack_id = "Rack ID"
number_of_columns = "Number columns"
number_of_rows = "Number rows"
vol_high_conc = 'Volume for Highest Concentration'
vol_low_conc = 'Volume for Lowest Concentration'
stock_parameters ='Stock Parameters'
sol_1_parameters = 'Solvent 1 Parameters'
sol_2_parameters = 'Solvent 2 Parameters'
location = 'Location'

for index, value in enumerate(concentration_df[id_header].tolist()):

    if value == number_of_columns:
        number_cols = int(concentration_df[details_header].tolist()[index])
    if value == number_of_rows:
        number_rows = int(concentration_df[details_header].tolist()[index])

    if value == stock_parameters:
        vol_init_stock = float(concentration_df[vol_high_conc].tolist()[index])
        vol_final_stock = float(concentration_df[vol_low_conc].tolist()[index])
        stock_location = concentration_df[location].tolist()[index]

    if value == sol_1_parameters:
        vol_init_sol_1 = float(concentration_df[vol_high_conc].tolist()[index])
        vol_final_sol_1 = float(concentration_df[vol_low_conc].tolist()[index])
        sol_1_location = concentration_df[location].tolist()[index]

    if value == sol_2_parameters and concentration_df[vol_high_conc].tolist()[index] != '':
        vol_init_sol_2 = float(concentration_df[vol_high_conc].tolist()[index])
        vol_final_sol_2 = float(concentration_df[vol_low_conc].tolist()[index])
        sol_2_location = concentration_df[location].tolist()[index]

def generate_table(number_cols, number_rows):
    table = []
    for y in range(number_rows):
        for x in range(number_cols):
            table.append(y*8 + x)
    return table

table = generate_table(number_cols,number_rows)

p1000.transfer(
    (vol_init_stock, vol_final_stock),
    stock_rack.wells(stock_location),
    reaction_rack.wells(table),
    air_gap=10)

p1000.transfer(
    (vol_init_sol_1, vol_final_sol_1),
    source_trough4row.wells(sol_1_location),
    reaction_rack.wells(table),
    air_gap=10)

for c in robot.commands():
    print(c)