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
reactants_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\Amines_Sulfonamides.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\solvents.csv")

def reactants_transfer(reactants, solvent):
    # Deck setup

    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    #tiprack_1000_3 = containers.load("tiprack-1000ul-H", "B1")
    source_trough4row = containers.load("trough-12row", "C2")
    rack_stock_reactants_1 = containers.load("FluidX_24_5ml", "A1", "R_1")
    rack_stock_reactants_2 = containers.load("FluidX_24_5ml", "A2", "R_2")
    rack_stock_reactants_3 = containers.load("FluidX_24_5ml", "B1", "R_3")
    rack_stock_reactants_4 = containers.load("FluidX_24_5ml", "B2", "R_4")
    reaction_rack = containers.load("Starlab_96_Square_2mL", "C1", "2mL_rack")
    trash = containers.load("point", "C3")

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

    location_header = "Location"
    volume_per_reaction_header = "volume_per_vial"
    rack_ID_header = "Rack ID"
    id_header = "CPD ID"
    solvent = "DMA"
    rack_1 = "24_rack1"
    rack_2 = "24_rack2"
    rack_3 = "24_rack3"
    rack_4 = "24_rack4"
    solvent_location_header = "Location_trough"
    solvent_volume_header = "Volume to dispense (uL)"
    counter = 0
    for i, x in enumerate(reactants_df[rack_ID_header].tolist()):
        volume_per_reaction = [reactants_df[volume_per_reaction_header].tolist()[i]]
        source_location = reactants_df[location_header].tolist()[i]

        if x == "":
            #print('null')
            break
        if x == rack_1:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_1.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        if x == rack_2:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_2.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        if x == rack_3:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_3.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        if x == rack_4:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_4.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        counter += 1
    # p1000.pick_up_tip()
    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            vol_to_add = [solvent_df[solvent_volume_header].tolist()[i]]
            solvent_loc = [solvent_df[solvent_location_header].tolist()[i]]

    #p1000.distribute(vol_to_add, source_trough4row.wells(solvent_loc),
     #                [x.top() for x in reaction_rack.wells(0, to=counter + 1)])
    #print(counter)
    robot.home()

reactants_transfer(reactants_df, solvent_df)
