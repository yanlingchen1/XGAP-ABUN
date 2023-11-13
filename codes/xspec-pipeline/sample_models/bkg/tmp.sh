statistic cstat
data 1:1 mos1S001-obj-SDSSTG3460_bkg-grp.pi
response  1:1 mos1S001-SDSSTG3460_bkg.rmf
arf 1:1 mos1S001-SDSSTG3460_bkg.arf

data 2:2 mos2S002-obj-SDSSTG3460_bkg-grp.pi
response  1:2 mos2S002-SDSSTG3460_bkg.rmf
arf 1:2 mos2S002-SDSSTG3460_bkg.arf

data 3:3 pnS003-obj-SDSSTG3460_bkg-grp.pi
response  1:3 pnS003-SDSSTG3460_bkg.rmf
arf 1:3 pnS003-SDSSTG3460_bkg.arf

data 4:4 rosat.pi
response  1:4 rosat.rsp

# spf + skybkg
response  2:1 ../mos1-diag.rsp
response  3:2 ../mos2-diag.rsp
response  4:3 ../pn-diag.rsp

# oot
response  5:3 pnS003-SDSSTG3460_bkg.rmf
arf 5:3 pnS003-SDSSTG3460_bkg.arf

# icm
response  6:1 mos1S001-SDSSTG3460_bkg.rmf
arf 6:1 mos1S001-SDSSTG3460_bkg.arf
response  6:2 mos2S002-SDSSTG3460_bkg.rmf
arf 6:2 mos2S002-SDSSTG3460_bkg.arf
response  6:3 pnS003-SDSSTG3460_bkg.rmf
arf 6:3 pnS003-SDSSTG3460_bkg.arf

ign 1:0.0-0.3,7.0-** 
ign 2:0.0-0.3,7.0-**
ign 3:0.0-0.3,7.0-**
ign bad

# ign instrumental lines
ign 1:1.2-1.85
ign 2:1.2-1.85
ign 3:1.2-1.55
ign 3:5.-**

# skybkg
mo constant*constant*(apec + TBabs(apec + powerlaw))

# spf+qpb
mo 2:m1_bg constant*constant*pow + atable{mos1S001-back-smoothed_savgol-140-5.mdl}
mo 3:m2_bg constant*constant*pow + atable{mos2S002-back-smoothed_savgol-140-5.mdl}
mo 4:pn_bg constant*constant*pow + atable{pnS003-back-smoothed_savgol-140-5.mdl}

# oot
mo 5:oot const*const*(pow+pow+apec+apec)

# icm
mo 6:icm constant*constant*TBabs*apec