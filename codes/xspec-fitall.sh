#!usr/bin/python
print('xspec parallel fitting begins!')
python xspec-pipeline/bkg-atable-pipeline/main_bkg1st_para.py
python xspec-pipeline/main_skybkg_para.py
python xspec-pipeline/bkg-atable-pipeline/main_bkg2st_para.py
python xspec-pipeline/main_icm_para.py

print('xspec parallel fitting ends!')