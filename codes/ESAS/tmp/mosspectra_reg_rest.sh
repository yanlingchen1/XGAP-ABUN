
mkdir /data/yanling/XGAP-ABUN/data/data/ID3460/reduction/SDSSTG3460/01r500
heainit
sasinit21

source set_chips_on.txt
source set_sas.txt

export M1=mos1S001
export M2=mos2S002

mkdir 01r500
mkdir 01r500/img
mkdir 01r500/logs
mkdir 01r500/diagnose
mkdir 01r500/mos_spec
mkdir 01r500/fitting

rm 01r500/logs/mosspectra_${M1}.log
rm 01r500/logs/mosspectra_${M2}.log

mosspectra eventfile=${M1}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/01r500-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M1}-bkgregtdet.fits masksky=${M1}-bkgregtsky.fits elow=700 ehigh=1200 ccds="${M1ON}" -V=7  > 01r500/logs/mosspectra_${M1}.log 2>&1
mosback inspecfile=${M1}-fovt.pi elow=700 ehigh=1200 ccds="${M1ON}" >> mosback_${M1}.log 2>&1 
mosspectra eventfile=${M2}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/01r500-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M2}-bkgregtdet.fits masksky=${M2}-bkgregtsky.fits elow=700 ehigh=1200 ccds="${M2ON}" -V=7 > 01r500/logs/mosspectra_${M2}.log 2>&1
mosback inspecfile=${M2}-fovt.pi elow=700 ehigh=1200 ccds="${M2ON}" >> mosback_${M2}.log 2>&1

for name in $M1 $M2
do
echo $name

mv $name*-700-1200* 01r500/img
mv $name*fovt.pi 01r500/01r500/$name-obj-SDSSTG3460_01r500.pi
mv $name*bkg.pi 01r500/01r500/$name-back-SDSSTG3460_01r500.pi
mv $name*.qdp 01r500/diagnose
mv $name*imt* 01r500/img
mv $name*.arf 01r500/01r500/$name-SDSSTG3460_01r500.arf
mv $name*.rmf 01r500/01r500/$name-SDSSTG3460_01r500.rmf
mv $name*imspdet* 01r500/img

done
done
