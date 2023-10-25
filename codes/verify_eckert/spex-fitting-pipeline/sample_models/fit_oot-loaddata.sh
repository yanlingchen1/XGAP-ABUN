# load data
data mos1S001-SDSSTG3460_bkg mos1S001-SDSSTG3460_bkg
data mos2S002-SDSSTG3460_bkg mos2S002-SDSSTG3460_bkg
data pnS003-SDSSTG3460_bkg pnS003-SDSSTG3460_bkg

# plot and bin data
pl dev xs
pl type dat
plot rx 0.2:10.
plot ry 1E-4:10.
pl x log
pl y log
ignore instrument 1 reg 2 1:1000000
ignore instrument 2 reg 2 1:1000000
ignore instrument 3 reg 2 1:1000000

ignore instrument 1 reg 1 0.:0.3 unit keV
ignore instrument 1 reg 1 7.:100. unit keV
ignore instrument 2 reg 1 0.:0.3 unit keV
ignore instrument 2 reg 1 7.:100. unit keV
ignore instrument 3 reg 1 0.:0.3 unit keV
ignore instrument 3 reg 1 7.:100. unit keV

# ignore the instrumental lines
ign instrument 1 reg 1 1.2:1.85 unit keV
ign instrument 2 reg 1 1.2:1.85 unit keV
ign instrument 3 reg 1 1.2:1.55 unit keV
ign instrument 3 reg 1 5.:100. unit keV

# obin will run into segmentation error
# obin instrument 1 region 1 0.3:7. unit kev
# obin instrument 2 region 1 0.3:7. unit kev
# obin instrument 3 region 1 0.3:7. unit kev

bin instrument 1 region 1 1:10000 20
bin instrument 2 region 1 1:10000 20
bin instrument 3 region 1 1:10000 20