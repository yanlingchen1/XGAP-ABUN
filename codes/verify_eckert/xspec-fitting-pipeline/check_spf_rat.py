'''
check spf ratio of 7-12 keV band in every observations
log the ratio and in every obs dir

https://www.cosmos.esa.int/web/xmm-newton/epic-scripts

'''

reduc_dir = f''
cp ~/Downloads/Fin_over_Fout.txt

chmod 755 Fin_over_Fout.txt

./Fin_over_Fout.txt mos1S001-allevc.fits mos2S002-allevc.fits pnS003-allevc.fits 7000 12000 Y myFinFout.dat
