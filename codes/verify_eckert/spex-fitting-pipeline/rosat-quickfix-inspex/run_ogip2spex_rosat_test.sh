export PHAFILE=rosat_poifix.pi
export RMFFILE=rosat_binfix.rsp
export SPOFILE=rosat.spo
export RESFILE=rosat.res

ogip2spex --phafile $PHAFILE --rmffile $RMFFILE --spofile $SPOFILE --resfile $RESFILE --keep-grouping
# ogip2spex --phafile $PHAFILE --rmffile $RMFFILE --arffile $ARFFILE --spofile $SPOFILE --resfile $RESFILE