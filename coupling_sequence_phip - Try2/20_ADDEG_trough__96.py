from opentrons import robot, containers, instruments
robot.head_speed(x=20000,  y=20000,  z=4000, a=100, b=700)

#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("96-PCR-flat", "B1")
reaction_rack2 = containers.load("96-PCR-flat", "C1")
reaction_rack3 = containers.load("96-PCR-flat", "D1")
reaction_rack4 = containers.load("96-PCR-flat", "E1")
trash = containers.load("point", "B3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=30,
    channels=8,
)
source_solvent = 'A8'
volume_solvent = 80
#source_water = 'A2'
#volume_water = 100
#source_aqueous = 'A11'
#volume_aqueous = 200
number_rows = 9
p300_multi.pick_up_tip()
p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack.rows(0,to=number_rows-1)], air_gap = 10, new_tip="never")
p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack2.rows(0,to=number_rows-1)], air_gap = 10,new_tip="never")
p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack3.rows(0,to=number_rows-1)], air_gap = 10,new_tip="never")
p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack4.rows(0,to=number_rows-1)], air_gap = 10,new_tip="never")
p300_multi.drop_tip()
#p300_multi.distribute(volume_water, source_trough4row.wells(source_water), [x.top() for x in reaction_rack.rows(0,to=number_rows-1)])

#p300_multi.pick_up_tip()
#p300_multi.aspirate (300, source_trough4row.wells(source_solvent))
#p300_multi.dispense (source_trough4row.wells(source_solvent))
#p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack.rows(0,to=number_rows-1)], air_gap=10)

#robot.pause()

#for i in range(0, number_rows):
#    p300_multi.pick_up_tip()
#    p300_multi.mix(5, 300, reaction_rack.rows(i).bottom(5))
#    p300_multi.drop_tip()
robot.home()