
source set_chips_on.txt
source set_sas.txt

export PN=pnS003
export ELO=700
export EHI=1200

for pat in 0 4
do

for regfile in spec_reg/reg0-mos1S001.reg
do
regname=$(basename $regfile | cut -d'-' -f 1)
echo $PN
echo $regname

rm ${regname}/logs/pnspectra_${pat}_${PN}.log
rm ${regname}/logs/pnback_${pat}_${PN}.log

pnspectra eventfile=${PN}-allevc.fits ootevtfile=${PN}-allevcoot.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/${regname}-${PN}.reg pattern=${pat} withsrcrem=yes maskdet=${PN}-bkgregtdet.fits masksky=${PN}-bkgregtsky.fits elow=${ELO} ehigh=${EHI} quads="${PNON}" -V=7 2>&1 | tee  ${regname}/logs/pnspectra_${pat}_${PN}.log
pnback inspecfile=${PN}-fovt.pi inspecoot=${PN}-fovtoot.pi elow=${ELO} ehigh=${EHI} quads="${PNON}" 2>&1 | tee ${regname}/logs/pnback_${pat}_${PN}.log 

rm -r ${regname}/${PN}_${pat}
mkdir ${regname}/${PN}_${pat}

mv pn*-${ELO}-${EHI}* ${regname}/${PN}_${pat}
mv pn*.pi ${regname}/${PN}_${pat}
mv pn*.qdp ${regname}/${PN}_${pat}
mv pn*imt* ${regname}/${PN}_${pat}
mv pn*.arf ${regname}/${PN}_${pat}
mv pn*.rmf ${regname}/${PN}_${pat}
mv pn*imspdet* ${regname}/${PN}_${pat}


cp ${regname}/${PN}_${pat}/${PN}-fovt.pi ${regname}/fitting/${PN}-${pat}-fovt.pi
cp ${regname}/${PN}_${pat}/${PN}-fovtoot.pi ${regname}/fitting/${PN}-${pat}-fovtoot.pi
cp ${regname}/${PN}_${pat}/${PN}-bkg.pi ${regname}/fitting/${PN}-${pat}-bkg.pi
cp ${regname}/${PN}_${pat}/${PN}.rmf ${regname}/fitting/${PN}-${pat}.rmf
cp ${regname}/${PN}_${pat}/${PN}.arf ${regname}/fitting/${PN}-${pat}.arf

done
done
