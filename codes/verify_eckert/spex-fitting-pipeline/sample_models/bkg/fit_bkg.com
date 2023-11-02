# save com
log save bins/bkg-bkg_2nd
log output logs/bkg-bkg

# load data
data PATH/epic-SDSSTG3460_bkg PATH/epic-SDSSTG3460_bkg

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

#### skybkg + icm + bkg ####
## inst mos1 ##
com reds
com hot
# lhb
com cie
# gh
com cie
# cxb
com pow
# icm 
com cie

# relate models
# gh
com rel 4 2
# cxb
com rel 5 2
# icm
com rel 6 1,2

# mos1 spf with 2nd resp
sect new
com 2 pow

## inst mos2 ##
sect copy 1

## mos2 spf with 2nd resp
sect copy 2

## inst pn ##
sect copy 1
# set bkg= cie+cie+pow+pow #
# bkg norm here 0.063*bkgfittingpar #
com 5 cie
com 5 cie
com 5 pow
com 5 pow

## pn spf ##
sect copy 2

### set region area ###
par -1 1 norm v BS-M1
par -1 2 norm v BS-M1
par -1 3 norm v BS-M2
par -1 4 norm v BS-M2
par -1 5 norm v BS-PN
par -1 6 norm v BS-PN

### reg 1: mos1###
abun aspl
# reds #
par 1 1 z v REDS
par 1 1 z s f
# hot #
par 1 2 nh v NH
par 1 2 nh s f
par 1 2 t s f
# lhb #
par 1 3 norm v 0.1
par 1 3 t v 0.11
par 1 3 t s f
# gh #
par 1 4 norm v 0.1
par 1 4 t v 0.2
# cxb #
par 1 5 gamm v 1.46
par 1 5 gamm s f
par 1 5 norm v 0.1
# icm #
par 1 6 norm v 1
par 1 6 t v 1
par 1 6 02:30 v 0.3
par 1 6 02:30 s f
### spf ###
par 2 1 norm v 1
par 2 1 gamm v 0.7
par 2 1 gamm s f
par 4 1 norm v 1
par 4 1 gamm v 0.7
par 4 1 gamm s f
par 6 1 norm v 1
par 6 1 gamm v 0.7
par 6 1 gamm s f
### couple par ###
# couple reds #
par 3 1 z couple 1 1 z
par 5 1 z couple 1 1 z
# couple hot #
par 3 2 nh couple 1 2 nh
par 3 2 t couple 1 2 t
par 5 2 nh couple 1 2 nh
par 5 2 t couple 1 2 t
## couple skybkg & icm ##
# couple lhb #
par 3 3 norm couple 1 3 norm
par 3 3 t couple 1 3 t
par 5 3 norm couple 1 3 norm
par 5 3 t couple 1 3 t
# couple gh #
par 3 4 norm couple 1 4 norm
par 3 4 t couple 1 4 t
par 5 4 norm couple 1 4 norm
par 5 4 t couple 1 4 t
# couple cxb #
par 3 5 norm couple 1 5 norm
par 3 5 gamm couple 1 5 gamm
par 5 5 norm couple 1 5 norm
par 5 5 gamm couple 1 5 gamm
# couple icm #
par 3 6 norm couple 1 6 norm
par 3 6 t couple 1 6 t
par 3 6 02:30 couple 1 6 02:30 
par 5 6 norm couple 1 6 norm
par 5 6 t couple 1 6 t
par 5 6 02:30 couple 1 6 02:30 

### set bkg in pn ###
par 5 7 norm v CIE1-n
par 5 7 t v CIE1-t
par 5 8 norm v CIE2-n
par 5 8 t v CIE2-t
par 5 9 norm v POW1-n
par 5 9 gamm v POW1-g
par 5 10 norm v POW2-n
par 5 10 gamm v POW2-g
par 5 7:10 norm s f
par 5 7:8 t s f
par 5 9:10 gamm s f

##### fit #####
calc
fit

##### output ######
log close save
log close output
log out bkg-bkg_freepar
par sho fre
log close output
log out bkg-bkg_allpar
par sho 
log close output
#### error #####
error 
log out bkg-
# make plot
plot frame new
plot frame 2
plot type chi
plot uy rel
plot view default f
plot view y 0:0.3
pl view x 0.075:0.925
plot cap id disp f
plot cap ut disp f
plot cap lt disp f
plot ry -1:1
plot frame 1
plot view default f
plot view y 0.3:0.9
plot dev cps bkg-bkg.ps
pl
pl close 2
# save plot data 
pl type data
pl x lin
pl y lin
pl adum dats/bkg-bkg

log close save
log close output
log out logs/bkg-bkg_freepar
par sho fre
log close output
log out logs/bkg-bkg_allpar
par sho 
log close output

# error
log out logs/bkg-bkg_error
#lhb#
error 1 3 norm
#gh#
error 1 4 t
error 1 4 norm
#cxb#
error 1 5 norm
#icm#
error 1 6 norm 
error 1 6 t
log close output
# make plot
plot frame new
plot frame 2
plot type chi
plot uy rel
plot view default f
plot view y 0:0.3
pl view x 0.075:0.925
plot cap id disp f
plot cap ut disp f
plot cap lt disp f
plot ry -1:1
plot frame 1
plot view default f
plot view y 0.3:0.9
plot dev cps bkg-bkg.ps
pl
pl close 2

# save plot data 
pl type data
pl x lin
pl y lin
pl adum dats/bkg-bkg


