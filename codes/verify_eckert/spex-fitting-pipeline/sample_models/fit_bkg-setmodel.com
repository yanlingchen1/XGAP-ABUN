#### skybkg + icm + oot ####

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
# spf
com pow


# relate models
# gh
rel 4 1,2
# cxb
rel 5 1,2
# icm
rel 6 1,2

# spf with 2nd resp
sect new
sect copy

## inst mos2 ##
???


## inst pn ##
sect new
sect copy
# oot= cie+cie+pow+pow
com cie
com cie
com pow
com pow




