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
        """
        if the annu is too small, use oot*sa.xcm, which only include 1 powerlaw
        """
        if self.regname < 'reg4':
            print('in sa')
            # Alter the inputs in sample_oot.xcm
            with open(f'{self.pipeline_path}/sample_models/oot/oot_ab_sa.xcm') as f:
                lines = f.read()
        else:
            print('not in sa')
            with open(f'{self.pipeline_path}/sample_models/oot/oot_ab.xcm') as f:
                lines = f.read()

        lines = self.add_gen_par(lines)
        with open(f'{self.savepath}/bins/oot_{self.regname}.xcm', 'w') as newf:
            newf.write(f'{lines}\n')
        
        with open(f'{self.pipeline_path}/sample_models/oot/oot_ab_mdl.xcm') as f:
            lines = f.read()

        lines = self.add_gen_par(lines)
        with open(f'{self.savepath}/bins/oot_{self.regname}_mdl.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''
xspec<<EOT
@bins/oot_{self.regname}.xcm
ipl
pl dat
wenv oot_{self.regname}
exit
exit
EOT''')
        os.system(f'''
ps2pdf oot_{self.regname}.ps
pdftk oot_{self.regname}.pdf cat 2 output 1.pdf
mv 1.pdf oot_{self.regname}.pdf
rm oot_{self.regname}.ps
mv oot_{self.regname}.pdf figs
mv oot_{self.regname}.pco dats
mv oot_{self.regname}.qdp dats 
''')
        print(f'PN-oot fitting for {self.regname} has finished!')

    def fit_bkg(self):
        # check rosat file
        if (not glob(f'{self.subdir}/rosat.pi')) or (not glob(f'{self.subdir}/rosat.rsp')):
            raise ValueError('Rosat spectrum and rmf has not been downloaded in bkg dir!')
        # Alter the inputs in sample_bkg.xcm
        with open(f'{self.pipeline_path}/sample_models/bkg/bkg_ab.xcm') as f:
            lines = f.read()
        #### general ####
        lines = self.add_gen_par(lines)
        #### oot ####
        lines = self.add_oot_xcm(lines)
        #### backscal ####
        lines = self.add_backscal(lines)
        with open(f'{self.savepath}/bins/bkg_{self.regname}.xcm', 'w') as newf:
            newf.write(f'{lines}\n')
        with open(f'{self.pipeline_path}/sample_models/bkg/bkg_ab_mdl.xcm') as f:
            lines = f.read()
        lines = self.add_gen_par(lines)
        with open(f'{self.savepath}/bins/bkg_{self.regname}_mdl.xcm', 'w') as newf:
            newf.write(f'{lines}\n')
        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''xspec<<EOT
@bins/bkg_{self.regname}.xcm
ipl
pl dat
wenv bkg_{self.regname}
exit
exit
EOT''')
        os.system(f'''
ps2pdf bkg_{self.regname}.ps
pdftk bkg_{self.regname}.pdf cat 2 output 1.pdf
mv 1.pdf bkg_{self.regname}.pdf
rm bkg_{self.regname}.ps
mv bkg_{self.regname}.pdf figs
mv bkg_{self.regname}.pco dats
mv bkg_{self.regname}.qdp dats 
''')
        print(f'bkg fitting for {self.regname} has finished!')
    

    def fit_qpb(self):        
        # Alter the inputs in sample_qpb_{inst_sname}.xcm
        for inst in self.insts:
            inst_sname = inst.split('S')[0]
            with open(f'{self.pipeline_path}/sample_models/qpb/qpb_{inst_sname}.xcm') as f:
                lines = f.read()
            #### general ####
            lines = self.add_gen_par(lines)
            with open(f'{self.savepath}/bins/qpb_{inst_sname}_{self.regname}.xcm', 'w') as newf:
                newf.write(f'{lines}\n')
            # Begin fitting
            os.chdir(self.savepath)
            os.system(f'''xspec<<EOT
@bins/qpb_{inst_sname}_{self.regname}.xcm
# save output data
ipl
setp energy
pl dat
wenv qpb_{inst_sname}_{self.regname}
exit
exit
EOT''')
            os.system(f'''
ps2pdf qpb_{inst_sname}_{self.regname}.ps
pdftk qpb_{inst_sname}_{self.regname}.pdf cat 2 output 1.pdf
mv 1.pdf qpb_{inst_sname}_{self.regname}.pdf
rm qpb_{inst_sname}_{self.regname}.ps
mv qpb_{inst_sname}_{self.regname}.pdf figs
mv qpb_{inst_sname}_{self.regname}.pco dats
mv qpb_{inst_sname}_{self.regname}.qdp dats 
    ''')
            print(f'qpb_{inst_sname} fitting for {self.regname} has finished!')
