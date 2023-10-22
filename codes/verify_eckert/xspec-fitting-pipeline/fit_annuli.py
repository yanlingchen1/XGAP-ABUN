from my_io import IO
from fit_other import FitOther
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd

fit_spec = FitOther()

class FitSpecICM(IO):
    def __init__(self, date, rootdir, srcname1, srcname2, regname, nH, reds, insts = ['mos1S001', 'mos2S002', 'pnS003']):
        super().__init__(date, rootdir, srcname1, srcname2, insts)
        self.regname = regname
        self.subdir = f'{rootdir}/{srcname2}_{regname}'
        self.inst_dict = self.get_backscal()
        self.pipeline_path = '/Users/eusracenorth/Documents/work/XGAP-ABUN/codes/verify_eckert/xspec-fitting-pipeline'
        self.nH = nH
        self.reds = reds
    
    def get_backscal(self):
        return fit_spec.get_backscal()

    def fit_1T(self):
        self.bkg_dict = self.load_bkgpar()
        print(self.regname)
        # Alter the inputs in sample_bkg.xcm
        with open(f'{self.pipeline_path}/sample_models/sample_data.xcm') as f:
            lines = f.readlines()
        newlines = [re.sub(r'SDSSTG828', self.srcname2, line) for line in lines]
        newlines = [re.sub(r'bkg', self.regname, line) for line in newlines]
        newlines = [re.sub(r'path', self.subdir, line) for line in newlines]
        newf = open(f'{self.savepath}/bins/annu_{self.regname}.xcm', 'w')
        for line in newlines:
            newf.write(f'{line}\n')
        
        #### oot ####
        value_data = []
        with open(f'{self.savepath}/logs/oot_{self.regname}_par.log', 'r') as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith('# '):
                if re.search(r'\d', line): 
                    columns = line.split()
                    if 'frozen' in line:
                        value = columns[-2]
                    else:
                        value = columns[-3]
                    value_data.append(value)


        # Write the Value data
        for i, value in enumerate(value_data):
            newf.write(f'new oot:{int(i+1)} {value}\n' )
        newf.write(f'free oot:1-14\n')
        newf.close()

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''xspec<<EOT
log >logs/annu_{self.regname}_fit.log
@bins/annu_{self.regname}.xcm

#### skybkg ####
# extract region area
new 1 {self.inst_dict['mos1S001']}
new 18 {self.inst_dict['mos2S002']}
new 35 {self.inst_dict['pnS003']}
new 7 {self.nH}
new oot:2 0.063

#### LHB ####
new 6 {self.bkg_dict['lhb-n']}
free 3,6
#### GH ####
new 8 {self.bkg_dict['gh-t']}
new 11 {self.bkg_dict['gh-n']}
free 8,11
#### cxb ####
new 17 {self.bkg_dict['cxb-n']}
free 16,17
#### spf ####
new spf:6 0
new spf:12 0
new spf:18 0
free spf:6,12,18
#### icm ####
new 12 1
new 15 1e-4
new 14 {self.reds}
free 14
thaw 12,13,15

### fit ###
fit 200 1e-2
setp energy
pl dat rat
ipl
pl dat
wenv annu_{self.regname}
exit
log none
save all bins/annu_{self.regname}_2nd.xcm
log >logs/annu_{self.regname}_allpar.log
sho par
log none
log >logs/annu_{self.regname}_freepar.log
sho fre
log none
chain length 1000
chain run annu_{self.regname}_chain1000.out
log >logs/annu_{self.regname}_chain1000_par.log
err 12,13,15
log none
cpd annu_{self.regname}.ps/ocps
setp rebin 3 30
pl lda ra
exit
EOT''')
        os.system(f'''
ps2pdf annu_{self.regname}.ps
rm annu_{self.regname}.ps
mv annu_{self.regname}.pdf figs
mv annu_{self.regname}.pco dats
mv annu_{self.regname}.qdp dats 
mv annu_{self.regname}_chain1000.out logs
''')
        print(f'annu fitting for {self.regname} has finished!')


