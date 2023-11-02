log close save
log close output
log out logs/oot-bkg_freepar
par sho fre
log close output
log out logs/oot-bkg_allpar
par sho 
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
plot dev cps figs/oot-bkg.ps
pl
pl close 2

# save plot data
pl type data
pl x lin
pl y lin
pl adum dats/oot-bkg

