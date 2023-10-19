import re
import pandas as pd

# Begin fitting
        os.chdir(self.savepath)
        os.system(f'''xspec<<EOT
log >logs/annu_{self.regname}_fit.log
@bins/annu_{self.regname}.xcm

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
wenv annu_{self.regname}
exit
log none
save all bins/annu_{self.regname}.xcm
y
log >logs/annu_{self.regname}_allpar.log
sho par
log none
log >logs/annu_{self.regname}_freepar.log
sho fre
log none
cpd annu_{self.regname}.ps/ocps
setp rebin 3 100
pl lda ra
exit
EOT''')
        os.system(f'''
ps2pdf annu_{self.regname}.ps
rm annu_{self.regname}.ps
mv annu_{self.regname}.pdf figs
mv annu_{self.regname}.pco dats
mv annu_{self.regname}.qdp dats 
''')
        print(f'annu fitting for {self.regname} has finished!')
