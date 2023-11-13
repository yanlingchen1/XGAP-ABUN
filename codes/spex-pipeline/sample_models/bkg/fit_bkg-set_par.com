### set region area ###
par -1 1 norm v {bs-m1}
par -1 2 norm v {bs-m1}
par -1 3 norm v {bs-m2}
par -1 4 norm v {bs-m2}
par -1 5 norm v {bs-pn}
par -1 6 norm v {bs-pn}

### reg 1: mos1###
abun aspl
# reds #
par 1 1 reds v {reds}
# hot #
par 1 2 nh v {nh}
par 1 2 nh s f
# lhb #
par 1 3 norm v 1e2
par 1 3 t v 0.11
par 1 3 t s f
# gh #
par 1 4 norm v 1e2
par 1 4 t v 0.2
# cxb #
par 1 5 gamm v 1.46
par 1 5 s f
par 1 5 norm v 1e3
# icm #
par 1 6 norm v 1e3
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
par 3 1 reds couple 1 1 reds
par 5 1 reds couple 1 1 reds
# couple hot #
par 3 2 nh couple 1 2 nh
par 3 2 t couple 1 2 t
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



### set oot in pn ###
par 5 7 norm v {cie1-n}
par 5 7 t v {cie1-t}
par 5 8 norm v {cie2-n}
par 5 8 t v {cie2-t}
par 5 9 norm v {pow1-n}
par 5 9 gamm v {pow1-g}
par 5 10 norm v {pow2-n}
par 5 10 gamm v {pow2-g}
par 5 7:10 norm s f
par 5 7:8 t s f
par 5 9:10 gamm s f

