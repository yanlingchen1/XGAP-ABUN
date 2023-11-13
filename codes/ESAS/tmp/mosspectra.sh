
source /data/yanling/XGAP-ABUN/data/data/ID3460/reduction/SDSSTG3460/codes/mosinit.sh
export M1=mos1S001
export M2=mos2S002

mkdir R500_01
mkdir R500_01/R500_01
mkdir R500_01/img
mkdir R500_01/logs
mkdir R500_01/diagnose

mosspectra eventfile=${M1}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/R500_01-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M1}-bkgregtdet.fits masksky=${M1}-bkgregtsky.fits elow=700 ehigh=1200 ccds="${M1ON}" -V=7 2>&1 |tee R500_01/logs/mosspectra_${M1}.log 
mosback inspecfile=${M1}-fovt.pi elow=700 ehigh=1200 ccds="${M1ON}" 2>&1  |tee mosback_${M1}.log 
mosspectra eventfile=${M2}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/R500_01-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M2}-bkgregtdet.fits masksky=${M2}-bkgregtsky.fits elow=700 ehigh=1200 ccds="${M2ON}" -V=7 2>&1 |tee R500_01/logs/mosspectra_${M2}.log
mosback inspecfile=${M2}-fovt.pi elow=700 ehigh=1200 ccds="${M2ON}" 2>&1  |tee mosback_${M2}.log 

for name in $M1 $M2
do
echo $name

mv $name*-700-1200* R500_01/img
mv $name*fovt.pi R500_01/R500_01/$name-obj-SDSSTG3460_R500_01.pi
mv $name*bkg.pi R500_01/R500_01/$name-back-SDSSTG3460_R500_01.pi
mv $name*.qdp R500_01/diagnose
mv $name*imt* R500_01/img
mv $name*.arf R500_01/R500_01/$name-SDSSTG3460_R500_01.arf
mv $name*.rmf R500_01/R500_01/$name-SDSSTG3460_R500_01.rmf
mv $name*imspdet* R500_01/img

done
