statistic cstat
# allbkg
data 1:1 mos1S001-obj-SDSSTG9647_R500_01-grp.pi
response 1:1 ../mos1-diag.rsp
response  5:1 mos1S001-SDSSTG9647_R500_01.rmf
arf 5:1 mos1S001-SDSSTG9647_R500_01.arf
data 2:2 mos2S002-obj-SDSSTG9647_R500_01-grp.pi
response 2:2 ../mos2-diag.rsp
response  5:2 mos2S002-SDSSTG9647_R500_01.rmf
arf 5:2 mos2S002-SDSSTG9647_R500_01.arf
data 3:3 pnS003-obj-0-SDSSTG9647_R500_01-grp.pi
response 3:3 ../pn-diag.rsp
response  5:3 pnS003-0-SDSSTG9647_R500_01.rmf
arf 5:3 pnS003-0-SDSSTG9647_R500_01.arf
data 4:4 pnS003-obj-4-SDSSTG9647_R500_01-grp.pi
response  5:4 pnS003-4-SDSSTG9647_R500_01.rmf
arf 5:4 pnS003-4-SDSSTG9647_R500_01.arf
response 4:4 ../pn-diag.rsp
response  6:3 pnS003-0-SDSSTG9647_R500_01.rmf
arf 6:3 pnS003-0-SDSSTG9647_R500_01.arf
response  6:4 pnS003-4-SDSSTG9647_R500_01.rmf
arf 6:4 pnS003-4-SDSSTG9647_R500_01.arf

ign 1:0.0-0.5,7.0-** 
ign 2:0.0-0.5,7.0-**
ign 3:0.0-0.5,2.0-**
ign 4:0.0-1.0,7.0-**
# ign instrumental lines
ign 1:1.2-1.85
ign 2:1.2-1.85
ign 3:1.2-1.55
ign 4:1.2-1.55
ign bad


@SAV/bins/annu_R500_01_MDL_mdl.xcm

#### areas #####
new icm:1 BS-M1
new icm:8 BS-M2
new icm:15 BS-PN
free icm:1,8,15
#### insts #####
new icm:2 1
new icm:9 1
new icm:16 1
free icm:2,9,16
#### nh ####
new icm:3 NH
new icm:10=icm:3
new icm:17=icm:3
free icm:3
#### reds ####
new icm:6 REDS
new icm:13=icm:6
new icm:20=icm:6
free icm:6
#### ICM ####
new icm:4 1
new icm:5 0.3
new icm:7 1e-4
new icm:11=icm:4
new icm:18=icm:4
new icm:12=icm:5
new icm:19=icm:5
new icm:14=icm:7
new icm:21=icm:7
thaw icm:4,icm:5,icm:7
#### allbkg ####
new m1_bg:1 1
new m2_bg:1 1
new pn_bg:1 1
free m1_bg:1,m2_bg:1,pn_bg:1
#### oot ####
new oot:1=icm:15
new oot:2=0.063*icm:16
new oot:3 POW1-g
new oot:4 POW1-n
new oot:5 POW2-g
new oot:6 POW2-n
new oot:7 CIE1-t
new oot:8 CIE1-abun
new oot:9 CIE1-reds
new oot:10 CIE1-n
new oot:11 CIE2-t
new oot:12 CIE2-abun
new oot:13 CIE2-reds
new oot:14 CIE2-n
free oot:1-14


### fit ###
fit 200 1e-2
setp energy
pl dat rat
log none
save all bins/annu_R500_01_MDL_2nd.xcm
log >logs/annu_R500_01_MDL_allpar.log
sho par
log none
log >logs/annu_R500_01_MDL_chain1000.out
chain length 1000
chain run annu_R500_01_MDL_chain1000.out
log none
log >logs/annu_R500_01_MDL_chain1000_par.log
err icm:4,icm:5,icm:7
log none
log >logs/annu_R500_01_MDL_freepar.log
sho fre
log none
cpd annu_R500_01_MDL.ps/ocps
setp rebin 3 30
pl lda ra