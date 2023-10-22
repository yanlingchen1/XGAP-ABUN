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

class FitFrame(IO):
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

    