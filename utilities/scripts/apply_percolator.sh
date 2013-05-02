#!/bin/bash
# Command line arguments:
# - script to produce the .pin file, with its full path (e.g sqt2pin, msgf2pin, etc)
# - target file directory 
# - extension of the target file (-target.mzid for msgf files)
# - decoy file directory
# - extension of the decoy file  (-decoy.mzid for msgf files)
# - full path to percolator executable 
# - directory including the output files 

# Notes: 
# - the percolator or convert options need to be changed by hand in this file  
# - the target and decoy file need to have the same name except for extension

# Command line arguments 
converter=$1
converter_options=$2
target_file_dir=$3
target_file_ext=$4
decoy_file_dir=$5
decoy_file_ext=$6
perc_path=$7
perc_options=$8
out_dir=$9
##########

# print the command line arguments 
echo -e "\n------------------------------------"
echo "Command line arguments:"
echo -e "------------------------------------"    
echo "converter=${converter}"
echo "converter_options=${converter_options}"
echo "target_file_dir=${target_file_dir}"
echo "target_file_ext=${target_file_ext}"
echo "decoy_file_dir=${decoy_file_dir}"
echo "decoy_file_ext=${decoy_file_ext}"
echo "percolator_path=${perc_path}"
echo "percolator_options=${perc_options}"
echo "out_dir=${out_dir}"
echo -e "------------------------------------"

# create the output folders
for d in ${out_dir} ${out_dir}/pin ${out_dir}/xml ${out_dir}/tab 
do
  if ! [ -d $d ]; then
    mkdir $d
  fi
done

for targetf in ${target_file_dir}/*${target_file_ext}
do
    base=`basename ${targetf} ${target_file_ext}`  
    decoyf=${decoy_file_dir}/${base}${decoy_file_ext}
    echo "-------- Processing $base ..."
           
    pinfile=${out_dir}/pin/$base.pin
    echo "Command: ${converter} ${converter_options} -o $pinfile $targetf $decoyf"
    ${converter} ${converter_options} -o $pinfile $targetf $decoyf
      
    xml_file=${out_dir}/xml/$base.xml
    tab_file=${out_dir}/tab/$base.tab
    echo -e "\nCommand: ${perc_path} $perc_options -X $xml_file $pinfile" 
    ${perc_path} $perc_options -X $xml_file $pinfile > $tab_file
    echo "-------- DONE."
done


