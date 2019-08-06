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
amines_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\amines_1_template.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\Solvents.csv")
#robot.reset()


def stock_solution_amines(amines, solvent):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    source_trough4row = containers.load("trough-12row", "C2")
    rack_stock_AM_1 = containers.load("FluidX_24_5ml", "A1", "AM_1")
    rack_stock_AM_2 = containers.load("FluidX_24_5ml", "A2", "AM_2")
    rack_stock_AM_3 = containers.load("FluidX_24_5ml", "A3", "AM_3")
    rack_stock_AM_4 = containers.load("FluidX_24_5ml", "B1", "AM_4")
    trash = containers.load("point", "C3")
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
    id_header = "CPD ID"
    solvent = "DMF"
    rack_1 = "24_rack1"
    rack_2 = "24_rack2"
    rack_3 = "24_rack3"
    rack_4 = "24_rack4"
    location_header = "Location_trough"
    destination_location_header = "Location"
    volume_stock_header = "Volume to dispense (exp) at 0.5M"

    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            solvent_location = solvent_df[location_header].tolist()[i]
    # robot.pause()
    for i, x in enumerate(amines_df[destination_location_header].tolist()):
        destination_location = x
        vol_to_dispense = [amines_df[volume_stock_header].tolist()[i]]
        amine_id = amines_df[rack_ID_header].tolist()[i]
        if amine_id == "":
            print ('null')
            break
        print (rack_ID_header, amine_id, vol_to_dispense)
        #p1000.pick_up_tip()
        if amine_id == rack_1:
            print ('rack1')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_AM_1.wells(destination_location).top(-5), new_tip='never')
        if amine_id == rack_2:
            print ('rack2')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_AM_2.wells(destination_location).top(-5), new_tip='never')
        if amine_id == rack_3:
            print ('rack3')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_AM_3.wells(destination_location).top(-5), new_tip='never')
        if amine_id == rack_4:
            print ('rack4')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location),
                               rack_stock_AM_4.wells(destination_location).top(-5), new_tip='never')
        #p1000.drop_tip()
    robot.home()
stock_solution_amines(amines_df, solvent_df)