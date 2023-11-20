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
    def __init__(self, date, rootdir, srcname1, srcname2, regname, nH, reds, insts = ['mos1S001', 'mos2S002', 'pnS003-0', 'pnS003-4']):
        super().__init__(date, rootdir, srcname1, srcname2, insts)
        self.regname = regname
        self.subdir = f'{rootdir}/{srcname2}_{regname}//{srcname2}_{regname}'
        self.inst_dict = self.get_backscal()
        self.pipeline_path = os.getcwd()
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
        self.subdir = f'{self.rootdir}/{self.srcname2}_{new_regname}/{self.srcname2}_{new_regname}'
        self.inst_dict = self.get_backscal()
    
    def add_gen_par(self, file):
        replace_dict = {'BS-PN':self.inst_dict['pnS003-0'], 'SRCNAME2': self.srcname2, 'REGNAME': self.regname, 'PATH': self.subdir}
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file

    def add_oot_com(self, file):
        value_data = []
        with open(f'{self.savepath}/logs/oot-{self.regname}_freepar.out', 'r') as f:
            lines = f.readlines()
        for line in lines:
            if 'thawn' in line:
                eles = line.split()[:]
                for i,ele in enumerate(eles):
                    if ele=='thawn':
                        value = float(eles[i-1])
                        value_data.append(value)

        # Write the Value data
        replace_dict = {}
        for i, name in enumerate(["CIE1-n", "CIE1-t", "CIE2-n", "CIE2-t", "POW1-n", "POW1-g", "POW2-n", "POW2-g"]):
            if '-n' in name:
                replace_dict[name] = value_data[i] * 0.063
            else:
                replace_dict[name] = value_data[i]

        # Alter the inputs
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file

    def add_backscal(self, file):
        """
        mode: 'bkg' or 'annu'
        appendix: '1T', '2T', 'GDEM'
        """

        # Write the Value data
        replace_dict = {"REDS":self.reds, "NH":self.nH, "BS-M1":self.inst_dict['mos1S001'], "BS-M2":self.inst_dict['mos2S002'], "BS-PN":self.inst_dict['pnS003-0']}

        # Alter the inputs in sample_oot.com
        for key, v in replace_dict.items():
            file = rep(file, key, f'{v}') 
        return file


    


    
