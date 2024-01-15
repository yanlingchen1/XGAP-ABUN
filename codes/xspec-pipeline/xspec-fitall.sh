#!usr/bin/python
heainit
conda activate xgap
spexinit
echo 'xspec parallel fitting begins!'
python xspec-pipeline/bkg-atable-pipeline/main_bkg1st_para.py
python xspec-pipeline/main_skybkg_para.py
python xspec-pipeline/bkg-atable-pipeline/main_bkg2nd_para.py
python xspec-pipeline/main_icm_para.py

echo 'xspec parallel fitting ends!'