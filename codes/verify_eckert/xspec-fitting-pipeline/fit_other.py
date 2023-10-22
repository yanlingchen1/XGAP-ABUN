from my_io import IO
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd


class FitOther(IO):

    def __init__(self, date, rootdir, srcname1, srcname2, regname, nH, reds, insts = ['mos1S001', 'mos2S002', 'pnS003']):
        super().__init__(date, rootdir, srcname1, srcname2, insts)
        self.regname = regname
        self.subdir = f'{rootdir}/{srcname2}_{regname}'
        self.inst_dict = self.get_backscal()
        self.pipeline_path = '/Users/eusracenorth/Documents/work/XGAP-ABUN/codes/verify_eckert/xspec-fitting-pipeline'
        self.nH = nH
        self.reds = reds
        
    def get_backscal(self):
        inst_dict = {}
        for name in self.insts:
            f = fits.open(f'{self.subdir}/{name}-back-{self.srcname2}_{self.regname}.pi')
            inst_dict[name] = np.round(f[1].header['BACKSCAL'] * (0.05/60) ** 2, 3)
        return inst_dict

    def update_inst_dict(self, new_regname):
        self.regname = new_regname
        self.subdir = f'{self.rootdir}/{self.srcname2}_{new_regname}'
        self.inst_dict = self.get_backscal()

    def fit_oot(self):
        # Alter the inputs in sample_oot.xcm
        with open(f'{self.pipeline_path}/sample_models/sample_oot.xcm') as f:
            lines = f.readlines()
        newlines = [re.sub(r'SDSSTG828', self.srcname2, line) for line in lines]
        newlines = [re.sub(r'bkg', self.regname, line) for line in newlines]
        newlines = [re.sub(r'path', self.subdir, line) for line in newlines]
        with open(f'{self.savepath}/bins/oot_{self.regname}.xcm', 'w') as newf:
            for line in newlines:
                newf.write(f'{line}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''xspec<<EOT
log >logs/oot_{self.regname}_fit.log
@bins/oot_{self.regname}.xcm
new 1 {self.inst_dict['pnS003']}
new 2 1
free 1,2
fit 100 1e-3
setp energy
pl dat rat
ipl
pl dat
wenv oot_{self.regname}
exit
log none
save all bins/oot_{self.regname}_2nd.xcm
log >logs/oot_{self.regname}_par.log
sho par
log none
cpd oot_{self.regname}.ps/ocps
setp rebin 3 20
pl lda ra
exit
EOT''')
        os.system(f'''
ps2pdf oot_{self.regname}.ps
rm oot_{self.regname}.ps
mv oot_{self.regname}.pdf figs
mv oot_{self.regname}.pco dats
mv oot_{self.regname}.qdp dats 
''')

        print(f'PN-oot fitting for {self.regname} has finished!')


    def fit_qpb_pn(self):        
        # Alter the inputs in sample_qpb_pn.xcm
        with open(f'{self.pipeline_path}/sample_models/sample_qpb_pn.xcm') as f:
            lines = f.readlines()
        newlines = [re.sub(r'SDSSTG828', self.srcname2, line) for line in lines]
        newlines = [re.sub(r'bkg', self.regname, line) for line in newlines]
        newlines = [re.sub(r'path', self.subdir, line) for line in newlines]
        with open(f'{self.savepath}/bins/qpb_pn_{self.regname}.xcm', 'w') as newf:
            for line in newlines:
                newf.write(f'{line}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''xspec<<EOT
log >logs/qpb_pn_{self.regname}_fit.log
@bins/qpb_pn_{self.regname}.xcm
@{self.pipeline_path}/sample_models/sample_qpb_pn_mdl.xcm
new 1 {self.inst_dict['pnS003']}
free 1
save all bins/qpb_pn_{self.regname}_mdl.xcm
thaw 2-40
# free gaussian lines
free 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38
free 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39
free 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40
# set brem
new 2 0.4
new 3 1e-5
# set bknpow
new 4 0.5
new 5 2
new 6 0.3
new 7 1e-5
sho par 
fit 100 1e-3
free 2-7
sho par
thaw 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40
fit 100 1e-3
sho par
log none
# save output data
ipl
setp energy
pl dat
wenv qpb_pn_{self.regname}
exit
# save exe file
save all bins/qpb_pn_{self.regname}.xcm
y
# save par
log >logs/qpb_pn_{self.regname}_par.log
sho par
log none
setplot energy
setpl rebin 20 1000
plot ld ra
cpd qpb_pn_{self.regname}.ps/ps
pl
exit
EOT''')
        os.system(f'''
ps2pdf qpb_pn_{self.regname}.ps
rm qpb_pn_{self.regname}.ps
mv qpb_pn_{self.regname}.pdf figs
mv qpb_pn_{self.regname}.pco dats
mv qpb_pn_{self.regname}.qdp dats 
    ''')

        print(f'PN-qpb_pn fitting for {self.regname} has finished!')

    def fit_qpb_mos(self):
        pass

    def fit_bkg(self):
        # check rosat file
        if (not glob(f'{self.subdir}/rosat.pi')) or (not glob(f'{self.subdir}/rosat.rsp')):
            raise ValueError('Rosat spectrum and rmf has not been downloaded in bkg dir!')

        # Alter the inputs in sample_bkg.xcm
        with open(f'{self.pipeline_path}/sample_models/sample_bkg.xcm') as f:
            lines = f.readlines()
        newlines = [re.sub(r'SDSSTG828', self.srcname2, line) for line in lines]
        newlines = [re.sub(r'bkg', self.regname, line) for line in newlines]
        newlines = [re.sub(r'path', self.subdir, line) for line in newlines]
        newf = open(f'{self.savepath}/bins/bkg_{self.regname}.xcm', 'w')
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
log >logs/bkg_{self.regname}_fit.log
@bins/bkg_{self.regname}.xcm

#### skybkg ####
# extract region area
new 1 {self.inst_dict['mos1S001']}
new 14 {self.inst_dict['mos2S002']}
new 27 {self.inst_dict['pnS003']}
new 7 {self.nH}
new oot:2 0.063
new icm:6 {self.reds}
### fit ###
fit 200 1e-2
setp energy
pl dat rat
ipl
pl dat
wenv bkg_{self.regname}
exit
log none
save all bins/bkg_{self.regname}_2nd.xcm
log >logs/bkg_{self.regname}_allpar.log
sho par
log none
log >logs/bkg_{self.regname}_freepar.log
sho fre
log none
cpd bkg_{self.regname}.ps/ocps
setp rebin 3 100
pl lda ra
exit
EOT''')
        os.system(f'''
ps2pdf bkg_{self.regname}.ps
rm bkg_{self.regname}.ps
mv bkg_{self.regname}.pdf figs
mv bkg_{self.regname}.pco dats
mv bkg_{self.regname}.qdp dats 
''')
        print(f'bkg fitting for {self.regname} has finished!')
    
    def load_bkgpar(self):
        df = pd.read_csv(f'{self.savepath}/csvs/cxb_par.csv')
        def judge_spf(norm):
            # ! always set spf to 0 for now
            return 0
            # if float(norm) < 1e-6:
            #     return 0
            # else:
            #     return norm
        outdict = {}
        for i, name in enumerate(df['Name']):
            outdict[name] = df['value'][i]
        
        outdict['spf-m1-n'] = judge_spf(outdict['spf-m1-n'])
        outdict['spf-m2-n'] = judge_spf(outdict['spf-m2-n'])
        outdict['spf-pn-n'] = judge_spf(outdict['spf-pn-n'])
        return dict

    