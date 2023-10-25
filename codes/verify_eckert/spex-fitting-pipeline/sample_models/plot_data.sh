pl dev xs
pl type dat
plot rx 0.1:10.
plot ry 1E-4:10.
pl x log
pl y log
ignore reg 2 1:1000000
ignore 0.:0.3 unit keV
ignore 10.:100. unit keV
# obin 0.3:10. unit kev
obin instrument 1 region 1 0.3:10. unit kev
bin instrument 1 region 1 1:10000 20

pl