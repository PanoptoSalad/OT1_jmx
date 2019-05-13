from opentrons import robot, containers, instruments


#containers.create(
#    "tiprack-300ul_storm2",                    # name of you container
#    grid=(8, 12),                    # specify amount of (columns, rows)
#    spacing=(9, 9),               # distances (mm) between each (column, row)
#    diameter=4,                     # diameter (mm) of each well on the plate
#    depth=60)                       # depth (mm) of each well on the plate
#containers.create(
#    "Starlab_96_Square_2mL",                    # name of you container
#    grid=(8, 12),                    # specify amount of (columns, rows)
#    spacing=(9, 9),               # distances (mm) between each (column, row)
#    diameter=8,                     # diameter (mm) of each well on the plate
#    depth=60)                       # depth (mm) of each well on the plate

containers.create(
    "StarLab_96_tall",                    # name of you container
    grid=(8, 12),                    # specify amount of (columns, rows)
    spacing=(18, 18),               # distances (mm) between each (column, row)
    diameter=11,                     # diameter (mm) of each well on the plate
    depth=46)                       # depth (mm) of each well on the plate