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

# relate models
# gh
com rel 4 1,2
# cxb
com rel 5 1,2
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
# set oot= cie+cie+pow+pow #
# oot norm here 0.063*ootfittingpar #
com 5 cie
com 5 cie
com 5 pow
com 5 pow

## pn spf ##
sect copy 2
