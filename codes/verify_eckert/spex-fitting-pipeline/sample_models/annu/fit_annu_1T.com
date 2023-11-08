var calc new
var calc qc

# save com
log save bins/annu-REGNAME-MDL_2nd
log output logs/annu-REGNAME-MDL

# load data
data PATH/epic-SRCNAME2_REGNAME PATH/epic-SRCNAME2_REGNAME

# plot and bin data
pl dev xs
pl type dat
plot rx 0.2:10.
plot ry 1E-4:10.
pl x log
pl y log

ignore instrument 1 reg 1 0.:0.5 unit keV
ignore instrument 1 reg 1 7.:100. unit keV
ignore instrument 1 reg 2 0.:0.5 unit keV
ignore instrument 1 reg 2 7.:100. unit keV
ignore instrument 1 reg 3 0.:0.5 unit keV
ignore instrument 1 reg 3 7.:100. unit keV

# ignore the instrumental lines
ign instrument 1 reg 1 1.2:1.85 unit keV
ign instrument 1 reg 2 1.2:1.85 unit keV
ign instrument 1 reg 3 1.2:1.55 unit keV
ign instrument 1 reg 3 5.:100. unit keV

# # obin will run into segmentation error
obin region 1 0.3:7. unit kev
obin region 2 0.3:7. unit kev
obin region 3 0.3:7. unit kev

# bin instrument 1 region 1 1:10000 20
# bin instrument 1 region 3 1:10000 20
# bin instrument 1 region 5 1:10000 20

# alter the data color 
# mos1-white, mos2-red, pn-green same as xspec
pl set 2
pl data col 02
pl set 3
pl data col 03

#### icm ####
## inst mos1 ##
com reds
com hot
# icm 
com cie

# relate models
# icm
com rel 3 1,2

## inst mos2 ##
sect copy 1


## inst pn ##
sect copy 1
# set REGNAME-MDL= cie+cie+pow+pow #
# REGNAME-MDL norm here 0.063*REGNAME-MDLfittingpar #
com 3 cie
com 3 cie
com 3 pow
com 3 pow

### set region area ###
par -1 1 norm v BS-M1
par -1 2 norm v BS-M2
par -1 3 norm v BS-PN

### reg 1: mos1###
abun aspl
# reds #
par 1 1 z v REDS
par 1 1 z s f
# hot #
par 1 2 nh v NH
par 1 2 nh s f
par 1 2 t s f
# icm #
par 1 3 norm v 10
par 1 3 t v 1
par 1 3 02:30 v 0.3
par 1 3 03:30 couple 1 3 02
par 1 3 02 s t

### couple par ###
# couple reds #
par 2 1 z couple 1 1 z
par 3 1 z couple 1 1 z
# couple hot #
par 2 2 nh couple 1 2 nh
par 2 2 t couple 1 2 t
par 3 2 nh couple 1 2 nh
par 3 2 t couple 1 2 t

# couple icm #
par 2 3 norm couple 1 3 norm
par 2 3 t couple 1 3 t
par 2 3 02:30 couple 1 3 02:30 
par 3 3 norm couple 1 3 norm
par 3 3 t couple 1 3 t
par 3 3 02:30 couple 1 3 02:30 

### set oot in pn ###
par 3 4 norm v CIE1-n
par 3 4 t v CIE1-t
par 3 5 norm v CIE2-n
par 3 5 t v CIE2-t
par 3 6 norm v POW1-n
par 3 6 gamm v POW1-g
par 3 7 norm v POW2-n
par 3 7 gamm v POW2-g
par 3 4:7 norm s f
par 3 4:5 t s f
par 3 6:7 gamm s f

### set distance ###
distance sector 3 REDS z

##### fit #####
calc
fit

##### output ######
log close save
log close output
log out logs/annu-REGNAME-MDL_freepar
par sho fre
log close output
log out logs/annu-REGNAME-MDL_allpar
par sho 
log close output

##### error ####
log out logs/annu-REGNAME-MDL_error
#icm#
error 1 3 norm:02
log close output

##### make plot ####
pl dev xs
plot dev cps annu-REGNAME-MDL.ps
pl type dat
plot rx 0.5:7.
plot ry 1E-4:1.
pl x log
pl y log
pl ry 1e-6:1
plot view default f
pl view x 0.1 0.9
plot frame new
plot frame 2
plot type chi
plot uy rel
plot view default f
plot view y 0:0.3
pl view x 0.1:0.9
plot cap id disp f
plot cap ut disp f
plot cap lt disp f
plot ry -5:5
plot rx 0.5:7.0
plot frame 1
plot view default f
plot view y 0.3:0.9
plot dev cps annu-REGNAME-MDL.ps
pl
pl close 2
# save plot data 
pl type data
pl x lin
pl y lin
pl adum dats/annu-REGNAME-MDL