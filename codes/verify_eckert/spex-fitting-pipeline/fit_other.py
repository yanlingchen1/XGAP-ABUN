from my_io import IO
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd
from fit_frame import FitFrame

class FitOther(FitFrame):
    def fit_oot(self):
        # Alter the inputs in sample_oot.com
        with open(f'{self.pipeline_path}/sample_models/oot/fit_oot.com') as f:
            lines = f.read()

        lines = lines.replace('REGNAME', self.regname)
        lines = self.add_gen_par(lines)
        with open(f'{self.savepath}/bins/oot-{self.regname}.com', 'w') as newf:
            newf.write(f'{lines}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''
rm logs/oot-{self.regname}* 
rm dats/oot-{self.regname}* 
rm figs/oot-{self.regname}* 
source /Users/eusracenorth/miniconda3/envs/spex/opt/spex/spex-activate.sh
spex<<EOT
log exe bins/oot-{self.regname}
quit
EOT''')
        os.system(f'''
ps2pdf oot-{self.regname}.ps
mv oot-{self.regname}.pdf figs/
rm oot-{self.regname}.ps
''')
        print(f'PN-oot fitting for {self.regname} has finished!')


    def fit_bkg(self):
        # check rosat file
        if (not glob(f'{self.subdir}/rosat.pi')) or (not glob(f'{self.subdir}/rosat.rsp')):
            raise ValueError('Rosat spectrum and rmf has not been downloaded in bkg dir!')

        # Alter the inputs in sample_bkg.com
        with open(f'{self.pipeline_path}/sample_models/bkg/fit_bkg.com') as f:
            lines = f.read()
        #### general ####
        lines = self.add_gen_par(lines)
        #### oot ####
        lines = self.add_oot_com(lines, '')
        #### backscal ####
        lines = self.add_backscal(lines)
        with open(f'{self.savepath}/bins/bkg-{self.regname}.com', 'w') as newf:
            newf.write(lines)

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''
source /Users/eusracenorth/miniconda3/envs/spex/opt/spex/spex-activate.sh
spex<<EOT
log exe bins/bkg-{self.regname}
quit
EOT''')
        os.system(f'''
ps2pdf bkg-{self.regname}.ps
mv bkg-{self.regname}.pdf figs/
rm bkg-{self.regname}.ps
''')
        print(f'bkg fitting for {self.regname} has finished!')

    
    