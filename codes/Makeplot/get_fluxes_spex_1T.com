com reds
com hot
# icm 
com cie

# relate models
# icm
com rel 3 1,2


par 1 1 z v REDS
par 1 1 z s f


par 1 2 nh v 0
par 1 2 nh s f
par 1 2 t s f


par 1 3 norm v NORM
par 1 3 t v TEMP
par 1 3 06:30 v 0.3
par 1 3 06:30 couple 1 3 26
par 1 3 26 v Abun

distance sector 1 REDS z
elim 0.5:2

log out PATH/logs/get_fluxes_spex_unabsflux_MDL overwrite
calc
par sho fre
log close output

par 1 2 nh v ABS
log out PATH/logs/get_fluxes_spex_absflux_MDL overwrite
calc
par sho fre
log close output
