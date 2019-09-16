from opentrons import robot, containers, instruments

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)


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


# Function that reads a csv file correctly without having to import anything (issues with molport). Uses 2 classes, Vector and DataFrame
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

# CSV file data
#solvent_df = read_csv(
#    r"C:\Users\opentrons\protocols\GitHub_repos\
#    OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\reaction_conditions.csv")
#rack_Ni_df = read_csv(
#    r"C:\Users\opentrons\protocols\GitHub_repos\
#    OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\Nirack.csv")

solvent_df = read_csv(
    r"csv\050919_JMX_56_reactions\reaction_conditions.csv")
rack_Ni_df = read_csv(
    r"csv\050919_JMX_56_reactions\Nirack.csv")

# Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "C2")
rack_stock_reactants_Ni = containers.load("FluidX_24_5ml_jmx", "B1", "R_3")
trash = containers.load("point", "B3")

# Pipettes SetUp
p1000 = instruments.Pipette(
    name='eppendorf1000',
    axis='b',
    trash_container=trash,
    tip_racks=[tiprack_1000],
    max_volume=1000,
    min_volume=30,
    channels=1,
)
rack_ID_header = "Rack ID"
id_header = "Reaction parameters type"
solvent = "Reaction solvent"
rack_3 = "24_rack3"
location_header = "Location_trough"
destination_location_header = "Location"
volume_stock_header = "Volume to dispense (exp) at 0.8M"

def stock_solution_reactant(reactants_df, solvent_df):

    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            solvent_location = solvent_df[location_header].tolist()[i]

    p1000.pick_up_tip()

    for i, x in enumerate(reactants_df[destination_location_header].tolist()):
        destination_location = x
        vol_to_dispense = [reactants_df[volume_stock_header].tolist()[i]]
        reactants_id = reactants_df[rack_ID_header].tolist()[i]
        if reactants_id == "":
            print ('null')
            break

        if reactants_id == rack_3:
            #print ('rack3')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_reactants_Ni.wells(destination_location).top(-5), new_tip='never', air_gap=10)

    p1000.drop_tip()

stock_solution_reactant(rack_Ni_df, solvent_df)

robot.home()

for c in robot.commands():
    print(c)