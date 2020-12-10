from opentrons import robot, containers, instruments

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)


class Vector(object):
    '''Storing and manipulating two-dimensional data'''
    def tolist(self):
        '''Convert vector object to list'''
        return list(self.input_list)

    def astype(self, input_type):
        '''Cast a vector to a specific type'''
        if input_type == int:
            return Vector([int(float(x)) for x in self.input_list])
        return Vector([input_type(x) for x in self.input_list])

    def __init__(self, input_list):
        self.input_list = input_list


class DataFrame(object):
    '''DataFrame class obtained from a dictionary'''
    
    def __len__(self):
        '''Get length of dataframe'''
        return self.length

    def __getitem__(self, value):
        '''Get a vector from dataframe based on value input'''
        return Vector(self.dict_input[value])

    def __init__(self, dict_input, length):
        self.dict_input = dict_input
        self.length = length


# Function that reads a csv file correctly without having to import anything (issues with molport). Uses 2 classes, Vector and DataFrame
def read_csv(input_file):
    '''reads a csv file, converts it into a dataframe'''
    lines = open(input_file).readlines()
    header = lines[0].rstrip().split(",") # get header from csv file by removing commas on first line
    out_d = {} # initiliase empty dictionary to add headers
    for head in header:
        out_d[head] = [] # initialise empty list to append values
    for line in lines[1:]:
        spl_line = line.rstrip().split(",") # remove commas from other lines
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i]) # values have been appended to list, as part of dictionary
    df = DataFrame(out_d, len(lines[1:])) # convert dictionary to dataframe
    return df

# CSV file data to dataframe
solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\reaction_conditions.csv")
rack_one_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\rack1.csv")
rack_two_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\rack2.csv")
rack_three_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\rack3.csv")

# Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
# tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "C2")
rack_stock_reactants_1 = containers.load("FluidX_24_5ml_jmx", "A1", "R_1")
rack_stock_reactants_2 = containers.load("FluidX_24_5ml_jmx", "A2", "R_2")
rack_stock_reactants_3 = containers.load("FluidX_24_5ml_jmx", "B1", "R_3")
# rack_stock_reactants_4 = containers.load("FluidX_24_5ml", "B2", "R_4")
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
# location of the reaction vessels/equipment
rack_ID_header = "Rack ID"
id_header = "Reaction parameters type"
solvent = "Reaction solvent"
rack_1 = "24_rack1"
rack_2 = "24_rack2"
rack_3 = "24_rack3"
# rack_4 = "24_rack4"
location_header = "Location_trough"
destination_location_header = "Location"
volume_stock_header = "Volume to dispense (exp) at 0.8M"

def stock_solution_reactant(reactants_df, solvent_df):
    '''Tells opentrons how to prepare stock solution'''
    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            solvent_location = solvent_df[location_header].tolist()[i] # tell OT1 where solvent is

    p1000.pick_up_tip() # OT1 gets ready to pipette

    for i, x in enumerate(reactants_df[destination_location_header].tolist()):
        destination_location = x # tell OT1 where to dispense the solvent to, to make reactants stock
        vol_to_dispense = [reactants_df[volume_stock_header].tolist()[i]]
        reactants_id = reactants_df[rack_ID_header].tolist()[i]
        if reactants_id == "":
            print ('null')
            break # exception handling, if empty rows are detected
        # print (rack_ID_header, reactants_id, vol_to_dispense)
        if reactants_id == rack_1: # read rack 1 conditions
            #print ('rack1')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location), # where to get solvent from
                               rack_stock_reactants_1.wells(destination_location).top(-5), new_tip='never', air_gap=10) # where to dispense solvent to
        if reactants_id == rack_2:
            #print ('rack2')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_reactants_2.wells(destination_location).top(-5), new_tip='never', air_gap=10)
        if reactants_id == rack_3:
            #print ('rack3')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_reactants_3.wells(destination_location).top(-5), new_tip='never', air_gap=10)
    p1000.drop_tip()


stock_solution_reactant(rack_one_df, solvent_df)
stock_solution_reactant(rack_two_df, solvent_df)
stock_solution_reactant(rack_three_df, solvent_df)

robot.home()

for c in robot.commands():
    print(c)
