var calc new
var calc qc

# save com
log save bins/annu-REGNAME-MDL_2nd
log output logs/annu-REGNAME-MDL

# load data
data PATH/epic-SRCNAME2_REGNAME PATH/epic-SRCNAME2_REGNAME

# plot and bin data
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
ignore instrument 1 reg 3 2.:100. unit keV
ignore instrument 1 reg 5 0.:1.0 unit keV
ignore instrument 1 reg 5 5.:100. unit keV

# ignore the instrumental lines
ign instrument 1 reg 1 1.2:1.85 unit keV
ign instrument 1 reg 2 1.2:1.85 unit keV
ign instrument 1 reg 3 1.2:1.55 unit keV
ign instrument 1 reg 5 1.2:1.55 unit keV

# ignore the reg4
ign instrument 1 reg 4 0.:100. unit keV
ign instrument 1 reg 6 0.:100. unit keV

## vbin to avoid 0 cts channel in ratio
## to solve pattern caused by 0cts channel-bkg
vbin inst 1 reg 1 0.5:7.0 2 2 un k
vbin inst 1 reg 2 0.5:7.0 2 1 un k
vbin inst 1 reg 3 0.5:2.0 2 1 un k
vbin inst 1 reg 5 1.0:5.0 2 1 un k

# alter the data color 
# mos1-white, mos2-red, pn-green same as xspec
pl set 2
pl data col 02
pl set 3
pl data col 03
pl set 5
pl data col 04

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


## inst pn pat0 ##
sect copy 1

## pn oot pat0 ##
sect new
com 4 cie
com 4 cie
com 4 pow
com 4 pow

## inst pn pat4 ##
sect copy 1


## pn oot pat4 ##
sect copy 4

### set region area ###
par -1 1 norm v BS-M1
par -1 2 norm v BS-M2
par -1 3 norm v BS-PN
par -1 5 norm v BS-PN

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
par 1 3 06:30 v 0.3
par 1 3 06:30 couple 1 3 26
par 1 3 26 s t

### couple par ###
# couple reds #
par 2 1 z couple 1 1 z
par 3 1 z couple 1 1 z
par 5 1 z couple 1 1 z
# couple hot #
par 2 2 nh couple 1 2 nh
par 2 2 t couple 1 2 t
par 3 2 nh couple 1 2 nh
par 3 2 t couple 1 2 t
par 5 2 nh couple 1 2 nh
par 5 2 t couple 1 2 t

# couple icm #
par 2 3 norm couple 1 3 norm
par 2 3 t couple 1 3 t
par 2 3 06:30 couple 1 3 06:30 
par 3 3 norm couple 1 3 norm
par 3 3 t couple 1 3 t
par 3 3 06:30 couple 1 3 06:30 
par 5 3 norm couple 1 3 norm
par 5 3 t couple 1 3 t
par 5 3 06:30 couple 1 3 06:30 

### set oot in pn ###
par 4 1 norm v CIE1-n
par 4 1 t v CIE1-t
par 4 2 norm v CIE2-n
par 4 2 t v CIE2-t
par 4 3 norm v POW1-n
par 4 3 gamm v POW1-g
par 4 4 norm v POW2-n
par 4 4 gamm v POW2-g
par 4 1:4 norm s f
par 4 1:2 t s f
par 4 3:4 gamm s f

### set oot in pn ###
par 6 1 norm v CIE1-n
par 6 1 t v CIE1-t
par 6 2 norm v CIE2-n
par 6 2 t v CIE2-t
par 6 3 norm v POW1-n
par 6 3 gamm v POW1-g
par 6 4 norm v POW2-n
par 6 4 gamm v POW2-g
par 6 1:4 norm s f
par 6 1:2 t s f
par 6 3:4 gamm s f

### set distance ###
distance sector 1:3 REDS z
distance sector 5 REDS z

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
error 1 3 norm:06
log close output

##### make plot ####
pl dev xs
pl set all
pl type dat
pl x log
pl y log
plot view default f
pl view x 0.1 0.9
plot view y 0.3:0.9
plot rx 0.5:7.0
plot ry 1E-6:1.
plot frame new
plot frame 2
plot type chi
plot uy rel
plot view default f
pl x log
plot view y 0:0.3
pl view x 0.1:0.9
plot ry -5:5
plot rx 0.5:7.0
plot cap id disp f
plot cap ut disp f
plot cap lt disp f

plot dev cps annu-REGNAME-MDL.ps
pl
pl close 1
# save plot data 
pl dev null
pl type data
pl x lin
pl y lin
pl adum dats/annu-REGNAME-MDL