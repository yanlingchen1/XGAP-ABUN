export PHAFILE=pnS003-obj-RGH80_bkg.pi
export BKGFILE=pnS003-back-RGH80_bkg.pi
export RMFFILE=pnS003-RGH80_bkg.rmf
export ARFFILE=pnS003-RGH80_bkg.arf
export SPOFILE=pnS003-obj-RGH80_bkg_withqpb.spo
export RESFILE=pnS003-obj-RGH80_bkg_withqpb.res

ogip2spex --phafile $PHAFILE --bkgfile $BKGFILE --rmffile $RMFFILE --arffile $ARFFILE --spofile $SPOFILE --resfile $RESFILE
# ogip2spex --phafile $PHAFILE --rmffile $RMFFILE --arffile $ARFFILE --spofile $SPOFILE --resfile $RESFILE