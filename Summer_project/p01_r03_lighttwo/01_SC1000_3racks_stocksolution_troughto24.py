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
solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\reaction_conditions.csv")
rack_one_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\rack1.csv")
rack_two_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\rack2.csv")
rack_three_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\rack3.csv")


def stock_solution_reactant(reactants_df, solvent_df):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "D2")
    #tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    source_trough4row = containers.load("trough-12row", "B2")
    rack_stock_reactants_1 = containers.load("FluidX_24_5ml", "A1", "R_1")
    rack_stock_reactants_2 = containers.load("FluidX_24_5ml", "A2", "R_2")
    rack_stock_reactants_3 = containers.load("FluidX_24_5ml", "B1", "R_3")
    #rack_stock_reactants_4 = containers.load("FluidX_24_5ml", "B2", "R_4")
    trash = containers.load("point", "B3")
    
    # Pipettes SetUp
    p1000 = instruments.Pipette(
        name='eppendorf1000',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000, tiprack_1000_2],
        max_volume=1000,
        min_volume=30,
        channels=1,
    )
    rack_ID_header = "Rack ID"
    id_header = "Reaction parameters type"
    solvent = "Reaction solvent"
    rack_1 = "24_rack1"
    rack_2 = "24_rack2"
    rack_3 = "24_rack3"
    #rack_4 = "24_rack4"
    location_header = "Location_trough"
    destination_location_header = "Location"
    volume_stock_header = "Volume to dispense (exp) at 0.8M"

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
        # print (rack_ID_header, reactants_id, vol_to_dispense)
        if reactants_id == rack_1:
            #print ('rack1')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_reactants_1.wells(destination_location).top(-5), new_tip='never', air_gap=10)
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
        #if reactants_id == rack_4:
            #print ('rack4')
            #if vol_to_dispense != 0:
                #p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               #rack_stock_reactants_4.wells(destination_location).top(-5), new_tip='never', air_gap=10)
    p1000.drop_tip()

    robot.home()

stock_solution_reactant(rack_one_df, solvent_df)
stock_solution_reactant(rack_two_df, solvent_df)
stock_solution_reactant(rack_three_df, solvent_df)

robot.commands()