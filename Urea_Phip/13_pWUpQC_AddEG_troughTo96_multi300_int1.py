from opentrons import robot, containers, instruments
robot.head_speed(x=17000,  y=17000,  z=5000, a=100, b=300)

#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
pwup_rack = containers.load("FluidX_96_small", "D1", "pwup rack")
destination_QC = containers.load("96-PCR-flat", "B1", "QC")
destination_screen = containers.load("Labcyte_384PP", "C1", "384_Screen")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=0,
    channels=8,
)
volume_QC = 20
volume_screen = 30
location_QC_solvent = 'A5'
volume_QC_solvent = 100
number_rows = 7

# The protocol itself
for i in range (0, number_rows+1):
    destination_384 = [destination_screen.rows(i).wells('A', length=8, step=2).bottom(1)]
    source_location = source_trough4row.wells(location_QC_solvent)
    p300_multi.transfer(volume_screen, source_location, destination_384, blow_out=True)
robot.home()
