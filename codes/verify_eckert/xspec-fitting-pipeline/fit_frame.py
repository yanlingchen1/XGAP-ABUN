from my_io import IO
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd

"""
This class shelter all the same function in both fitting functions
The fitting class should inherit from this class. 
"""

def rep(file, oldv, newv):
    return file.replace(oldv, newv)

class FitFrame(IO):
    def __init__(self, date, rootdir, srcname1, srcname2, regname, nH, reds, insts = ['mos1S001', 'mos2S002', 'pnS003']):
        super().__init__(date, rootdir, srcname1, srcname2, insts)
        self.regname = regname
        self.subdir = f'{rootdir}/{srcname2}_{regname}'
        self.inst_dict = self.get_backscal()
        self.pipeline_path = '/Users/eusracenorth/Documents/work/XGAP-ABUN/codes/verify_eckert/xspec-fitting-pipeline'
        self.nH = nH
        self.reds = reds
        self.bkg_dict = self.load_bkgpar()

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

    def add_gen_par(self, file):
        replace_dict = {'BS-PN':self.inst_dict['pnS003'], 'SRCNAME2': self.srcname2, 'REGNAME': self.regname, 'PATH': self.subdir, 'PIP':self.pipeline_path}
        print(replace_dict['PIP'])
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file
    
    def add_oot_xcm(self, file):
        #### oot ####
        value_data = []
        with open(f'{self.savepath}/logs/oot_{self.regname}_par.log', 'r') as f:
            lines = f.readlines()
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
        replace_dict = {}
        for i, name in enumerate(["POW1-g", "POW1-n",  "POW2-g", "POW2-n",  "CIE1-t", "CIE1-abun", "CIE1-reds", "CIE1-n",  "CIE2-t", "CIE2-abun", "CIE2-reds", "CIE2-n"]):
            if '-n' in name:
                replace_dict[name] = value_data[i+2]
            else:
                replace_dict[name] = value_data[i+2]

        # Alter the inputs
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file
    
    def add_backscal(self, file):
        """
        mode: 'bkg' or 'annu'
        mdl: '1T', '2T', 'GDEM'
        """

        # Write the Value data
        replace_dict = {"REDS":self.reds, "NH":self.nH, "BS-M1":self.inst_dict['mos1S001'], "BS-M2":self.inst_dict['mos2S002'], "BS-PN":self.inst_dict['pnS003']}

        # Alter the inputs in sample_oot.com
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file

    def add_gen_bkgpar(self, file):
        replace_dict = {'LHB-n':self.bkg_dict['lhb-n'], 'GH-n':self.bkg_dict['gh-n'], 'GH-t':self.bkg_dict['gh-t'], 'CXB-n':self.bkg_dict['cxb-n'], 
'SP-M1':self.bkg_dict['sp-m1-n'], 'SP-M2':self.bkg_dict['sp-m2-n'], 'SP-PN':self.bkg_dict['sp-pn-n']}
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file

    