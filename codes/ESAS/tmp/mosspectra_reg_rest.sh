
source set_chips_on.txt
source set_sas.txt

export ELO=700
export EHI=1200
export M1=mos1S001
export M2=mos2S002

for regfile in spec_reg/reg0-mos1S001.reg
do
regname=$(basename $regfile | cut -d'-' -f 1)

echo $regname

mkdir ${regname}
mkdir ${regname}/img
mkdir ${regname}/logs
mkdir ${regname}/diagnose
mkdir ${regname}/mos_spec
mkdir ${regname}/fitting

rm ${regname}/logs/mosspectra_${M1}.log
rm ${regname}/logs/mosspectra_${M2}.log

mosspectra eventfile=${M1}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/${regname}-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M1}-bkgregtdet.fits masksky=${M1}-bkgregtsky.fits elow=${ELO} ehigh=${EHI} ccds="${M1ON}" -V=7  >> ${regname}/logs/mosspectra_${M1}.log 2>&1
mosback inspecfile=${M1}-fovt.pi elow=${ELO} ehigh=${EHI} ccds="${M1ON}" >> mosback_${M1}.log 2>&1 
mosspectra eventfile=${M2}-allevc.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/${regname}-${M1}.reg pattern=12 withsrcrem=yes maskdet=${M2}-bkgregtdet.fits masksky=${M2}-bkgregtsky.fits elow=${ELO} ehigh=${EHI} ccds="${M2ON}" -V=7 >> ${regname}/logs/mosspectra_${M2}.log 2>&1
mosback inspecfile=${M2}-fovt.pi elow=${ELO} ehigh=${EHI} ccds="${M2ON}" >> mosback_${M2}.log 2>&1

for name in $M1 $M2
do
echo $name

mv ${name}*-${ELO}-${EHI}* ${regname}/img
mv ${name}*.pi ${regname}/mos_spec
mv ${name}*.qdp ${regname}/diagnose
mv ${name}*imt* ${regname}/img
mv ${name}*.arf ${regname}/fitting
mv ${name}*.rmf ${regname}/fitting
mv ${name}*imspdet* ${regname}/img

cp ${regname}/mos_spec/${name}-fovt.pi ${regname}/fitting
cp ${regname}/mos_spec/${name}-bkg.pi ${regname}/fitting

done
done
