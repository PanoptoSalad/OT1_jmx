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
reactants_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\amines.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\solvents.csv")

def reactants_transfer(reactants, solvent):
    # Deck setup

    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    #tiprack_1000_3 = containers.load("tiprack-1000ul-H", "B1")
    reaction_rack = containers.load("Starlab_96_Square_2mL", "D1")
    destination_rack1 = containers.load("StarLab_96_tall", "A1")
    destination_rack2 = containers.load("StarLab_96_tall", "B1")
    destination_rack3 = containers.load("StarLab_96_tall", "C1")
    trash = containers.load("point", "C3")


    # Pipettes SetUp
    p1000 = instruments.Pipette(
        name='eppendorf1000_no_min',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000, tiprack_1000_2],
        max_volume=1000,
        min_volume=0,
        channels=1,
    )
    id_header = "reaction"
    reaction_to_start = "Coupling_urea_sulpho"
    split_volume_header = "split 2 volume to add per vial"
    split_number_header = "split 2 number"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_per_vial = float(reaction_conditions_df[split_volume_header].tolist()[index])
            number_vials = int(reaction_conditions_df[split_number_header].tolist()[index])

            for i in range(0, number_vials):
                source_location = reaction_rack.wells(i).bottom(1)
                destination_1 = [x.top() for x in destination_rack1.rows(0, to=number_rows - 1)]

        # source_location1 = [well.bottom(4) for well in reaction_rack.rows(0, to=number_rows-1)]
        source_location1 = [reaction_rack.rows(0).bottom(4)]
        source_location2 = [reaction_rack.rows(1).bottom(4)]
        source_location3 = [reaction_rack.rows(2).bottom(4)]

        destination_1 = [x.top() for x in destination_rack1.rows(0, to=number_rows - 1)]
        destination_2 = [x.top() for x in destination_rack2.rows(0, to=number_rows - 1)]
        destination_3 = [x.top() for x in destination_rack1.rows(0, to=number_rows - 1)]
    p1000.distribute(volume_per_vial, source_row.wells(source_location),
                     [x.top(-15) for x in reaction_rack.rows(i).wells(0, to=number_cols)])

    for index, value in enumerate(row_loc_list):
        source_location = x
        volume_to_dispense = [row_vol_list[i]]
        p1000.distribute(volume_to_dispense, source_row.wells(source_location), [x.top(-15) for x in reaction_rack.rows(i).wells(0, to=number_cols)])
    #for i, x in enumerate(col_loc_list):
     #   source_location = x
     #   volume_to_dispense = [col_vol_list[i]]
     #   p1000.distribute(volume_to_dispense, source_col.wells(source_location), [x.top(-15) for x in reaction_rack.cols(i).wells(0, to=number_rows)])
    robot.home()

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