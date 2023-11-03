mkdir PATH/trafo_epic_loadqpbonly
mv PATH/epic* PATH/trafo_epic_loadqpbonly
source /Users/eusracenorth/miniconda3/envs/spex/opt/spex/spex-activate.sh
trafo<<EOT
1
3
100000
3
1 1
1
n
PATH/mos1S001-obj-SRCNAME_REGNAME.pi
y
PATH/mos1S001-allbkg-SRCNAME_REGNAME.pi
y
PATH/mos1S001-SRCNAME_REGNAME.rmf
1e-5 5e-3
1
y
PATH/mos1S001-SRCNAME_REGNAME.arf
0
2 2
1
n
PATH/mos2S002-obj-SRCNAME_REGNAME.pi
y
PATH/mos2S002-allbkg-SRCNAME_REGNAME.pi
y
PATH/mos2S002-SRCNAME_REGNAME.rmf
1e-5 5e-3
1
y
PATH/mos2S002-SRCNAME_REGNAME.arf
0
3 3
1
n
PATH/pnS003-obj-SRCNAME_REGNAME.pi
y
PATH/pnS003-allbkg-SRCNAME_REGNAME.pi
y
PATH/pnS003-SRCNAME_REGNAME.rmf
1
y
PATH/pnS003-SRCNAME_REGNAME.arf
0
PATH/epic-SRCNAME_REGNAME
PATH/epic-SRCNAME_REGNAME
EOT