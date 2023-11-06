from atable_allbkg import AtableBKG
from glob import glob


date = 231019

## Some mandatory parameters
nH_dict = {'SDSSTG3460':0.024, 'SDSSTG9647':0.0201, 'SDSSTG828':0.0303, 'RGH80':0.0131}
reds_dict = {'SDSSTG3460':0.043, 'SDSSTG9647':0.023, 'SDSSTG828':0.046, 'RGH80':0.037}

# ###  Some basic prefixes
# ### RGH80 ####
# srcname1 = ''
# srcname2 = 'RGH80'
# root_dir = f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/RGH80/eckert/0105860101"
# nH = nH_dict[srcname2]
# reds = reds_dict[srcname2]

#### IDxxx ####
for srcnum in ['3460']: # '3460', '9647', '828'
    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'
    root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

# ######### run program ############
nH = nH_dict[srcname2]
reds = reds_dict[srcname2]
ab = AtableBKG(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
# ab.bkgsmooth()
# ab.gen_qpbmdltxt()
# for i in range(13):
#     ab.update_inst_dict(f'reg{i}')
#     ab.atable_allbkg()
#     ab.qdp2ogip()

#### check the sum bkg file in xspec in every subdir ####
for i in range(13):
    ab.update_inst_dict(f'reg{i}')
    ab.qpb2txt()
