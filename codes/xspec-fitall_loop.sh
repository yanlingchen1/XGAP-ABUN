#!usr/bin/python
heainit
conda activate xgap
spexinit
echo 'xspec parallel fitting begins!'
python xspec-pipeline/bkg-atable-pipeline/main_bkg1stpy
python xspec-pipeline/main_skybkgpy
python xspec-pipeline/bkg-atable-pipeline/main_bkg2ndpy
python xspec-pipeline/main_icmpy

echo 'xspec parallel fitting ends!'
