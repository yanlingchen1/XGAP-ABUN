# save com
log save bkg-bkg
log output bkg-bkg

# load data
data epic-SDSSTG3460_bkg epic-SDSSTG3460_bkg

# plot and bin data
pl dev xs
pl type dat
plot rx 0.2:10.
plot ry 1E-4:10.
pl x log
pl y log
ignore instrument 1 reg 2 1:1000000
ignore instrument 1 reg 4 1:1000000
ignore instrument 1 reg 6 1:1000000

ignore instrument 1 reg 1 0.:0.5 unit keV
ignore instrument 1 reg 1 7.:100. unit keV
ignore instrument 1 reg 3 0.:0.5 unit keV
ignore instrument 1 reg 3 7.:100. unit keV
ignore instrument 1 reg 5 0.:0.5 unit keV
ignore instrument 1 reg 5 7.:100. unit keV

# ignore the instrumental lines
ign instrument 1 reg 1 1.2:1.85 unit keV
ign instrument 1 reg 3 1.2:1.85 unit keV
ign instrument 1 reg 5 1.2:1.55 unit keV
ign instrument 1 reg 5 5.:100. unit keV

# # obin will run into segmentation error
# obin region 1 0.3:7. unit kev
# obin region 3 0.3:7. unit kev
# obin region 5 0.3:7. unit kev

bin instrument 1 region 1 1:10000 20
bin instrument 1 region 3 1:10000 20
bin instrument 1 region 5 1:10000 20

# alter the data color 
# mos1-white, mos2-red, pn-green same as xspec
pl set 3
pl data col 02
pl set 5
pl data col 03

