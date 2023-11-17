
#!/bin/bash
heainit
sasinit21
source /data/yanling/XGAP-ABUN/data/data/ID828/reduction/SDSSTG828/set_chips_on.txt
source /data/yanling/XGAP-ABUN/data/data/ID828/reduction/SDSSTG828/set_sas.txt
#### MOS ####
export M1=mos1S001
export M2=mos2S002

mkdir R500_01
mkdir R500_01/R500_01
mkdir R500_01/img
mkdir R500_01/logs
mkdir R500_01/diagnose

# mosspectra eventfile=${M1}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/R500_01-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M1}-bkgregtdet.fits masksky=${M1}-bkgregtsky.fits elow=700 ehigh=1200 ccds="${M1ON}" -V=7 2>&1 |tee R500_01/logs/mosspectra_${M1}.log 
# mosback inspecfile=${M1}-fovt.pi elow=700 ehigh=1200 ccds="${M1ON}" 2>&1  |tee mosback_${M1}.log 
mosspectra eventfile=${M2}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/R500_01-${M2}.reg pattern=12 withsrcrem=yes maskdet=${M2}-bkgregtdet.fits masksky=${M2}-bkgregtsky.fits elow=700 ehigh=1200 ccds="${M2ON}" -V=7 2>&1 |tee R500_01/logs/mosspectra_${M2}.log
mosback inspecfile=${M2}-fovt.pi elow=700 ehigh=1200 ccds="${M2ON}" 2>&1  |tee mosback_${M2}.log 

for name in $M2
do
echo $name

mv $name*-700-1200* R500_01/img
mv $name-fovt.pi R500_01/R500_01/$name-obj-SDSSTG828_R500_01.pi
mv $name-bkg.pi R500_01/R500_01/$name-back-SDSSTG828_R500_01.pi
mv $name*.qdp R500_01/diagnose
mv $name*imt* R500_01/img
mv $name*.arf R500_01/R500_01/$name-SDSSTG828_R500_01.arf
mv $name*.rmf R500_01/R500_01/$name-SDSSTG828_R500_01.rmf
mv $name*imspdet* R500_01/img
done

#### PN ####
heainit
sasinit20
source /data/yanling/XGAP-ABUN/data/data/ID828/reduction/SDSSTG828/set_chips_on.txt
source /data/yanling/XGAP-ABUN/data/data/ID828/reduction/SDSSTG828/set_sas.txt
export name=pnS003
cp $name-allevc.fits $name-clean.fits
cp $name-allevcoot.fits $name-clean-oot.fits
cp $name-corevc.fits $name-corn.fits
cp $name-corevcoot.fits $name-corn-oot.fits
cp $name-bkgregtdet.fits sas20-pn-test/$name-bkg_region-sky.fits 
cp $name-bkgregtsky.fits sas20-pn-test/$name-bkg_region-det.fits 

for PAT in 0 4
do
pn-spectra prefix='S003' caldb=/data/yanling/sas20/esas-caldb region=spec_reg/R500_01-pnS003.reg mask=1 elow=700 ehigh=1200 pattern=4 quad1=1 quad2=1 quad3=1 quad4=1 2>&1 | tee R500_01/logs/pnspectra_$PAT.log
pn_back prefix=S003 caldb=/data/yanling/sas20/esas-caldb diag=0 elow=700 ehigh=1200 pattern=4 quad1=1 quad2=1 quad3=1 quad4=1 2>&1 | tee R500_01/logs/pnback_$PAT.log

mkdir R500_01/img/pn_$PAT
mkdir R500_01/diagnose/pn_$PAT

mv $name*-700-1200* R500_01/img/pn_$PAT
mv $name-obj.pi R500_01/R500_01/$name-obj-$PAT-SDSSTG828_R500_01.pi
mv $name-obj-oot.pi R500_01/R500_01/$name-obj-oot-$PAT-SDSSTG828_R500_01.pi
mv $name-back.pi R500_01/R500_01/$name-back-$PAT-SDSSTG828_R500_01.pi
mv $name*.qdp R500_01/diagnose/pn_$PAT
mv $name*imt* R500_01/img/pn_$PAT
mv $name*.arf R500_01/R500_01/$name-$PAT-SDSSTG828_R500_01.arf
mv $name*.rmf R500_01/R500_01/$name-$PAT-SDSSTG828_R500_01.rmf
mv $name*imspdet* R500_01/img/pn_$PAT

done
