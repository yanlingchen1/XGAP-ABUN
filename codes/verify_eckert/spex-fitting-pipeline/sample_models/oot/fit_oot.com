var calc new
var calc qc

# save com
log save bins/oot-REGNAME_2nd
log output logs/oot-REGNAME

# save fit log

# load data
data PATH/pnS003-oot-SRCNAME2_REGNAME PATH/pnS003-oot-SRCNAME2_REGNAME

# bin data
ignore 0.:0.5 unit keV
ignore 5.:100. unit keV

# ignore the instrumental lines
ign 1.2:1.55 unit keV

# obin will run into segmentation error
# obin 0.5:5. unit kev

bin 1:10000 20

pl dev xs
plot dev cps oot-REGNAME.ps
pl type dat
plot rx 0.4:10.
plot ry 1E-4:10.
pl x log
pl y log

com cie
com cie
com pow
com pow

par -1 1 norm v 10.287
par 1 1 norm v 0.1
par 1 2 norm v 0.1
par 1 3 norm v 0.1
par 1 4 norm v 0.1

calc
fit

log close save
log close output
log out logs/oot-REGNAME_freepar
par sho fre
log close output
log out logs/oot-REGNAME_allpar
par sho 
log close output

# make plot
pl ry 1e-6:1
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
plot ry -3:3
plot frame 1
plot view default f
plot view y 0.3:0.9
pl view x 0.1:0.9
plot dev cps oot-REGNAME.ps
pl
pl close 2

# save plot data
pl type data
pl x lin
pl y lin
pl adum dats/oot-REGNAME