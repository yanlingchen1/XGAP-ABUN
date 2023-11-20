#!usr/bin/python
heainit
conda activate xgap
spexinit
echo 'xspec parallel fitting begins!'
#python xspec-pipeline/bkg-atable-pipeline/main_bkg1st.py
#python xspec-pipeline/main_skybkg.py
#python xspec-pipeline/bkg-atable-pipeline/main_bkg2nd.py
python xspec-pipeline/main_icm.py

echo 'xspec parallel fitting ends!'
