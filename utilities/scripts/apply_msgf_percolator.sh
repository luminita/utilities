#!/bin/bash
# This script applies msgf+ and percolator on mzml data 
# Command line arguments:
# - directory containing the mzml files to be analyzed 
# -

## INPUT DATA
mzml_dir=$1
target_db=$2
decoy_db=$3
# example of options for QExactive data: 
# -inst 3 -t 10ppm -protocol 0 -tda 0 -ti 0,2 -e 1 -ntt 2 -n 1 -addFeatures 1 -m 3 -thread 3 -minLength 8 -maxLength 100"
# make sure that these are given between ""
msgf_options=$4
msgf_path=$5
# path to percolator and masg2pin 
perc_install=$6
out_dir=$7


print_args()
{
    echo -e "\n------------------------------------"
    echo "apply_msgf_percolator.sh parameters:"
    echo -e "------------------------------------"    
    echo "mzml_dir=${mzml_dir}"
    echo "target_db=${target_db}"
    echo "decoy_db=${decoy_db}"
    echo "msgf_options=${msgf_options}"
    echo "msgf_path=${msgf_path}"
    echo "percolator_install_path=${perc_install}"
    echo "out_dir=${out_dir}"
    echo -e "------------------------------------"
}


apply_msgf()
{
  # apply msgf+
  msgf_folder=${out_dir}/msgf
  for d in ${msgf_folder}; do
    if ! [ -d $d ]; then
      mkdir $d
    fi
  done

  echo -e "\n---- MSGF+"
  for mzml in ${mzml_dir}/*.mzML
  do
    base=`basename $mzml .mzML`
    echo -e "\n--Processing $base ..."

    target_file=${msgf_folder}/$base-target.mzid
    echo "Command: java -Xmx2500M -jar $msgf_path -s $mzml -d ${target_db} -o $target_file $msgf_options"
    java -Xmx2500M -jar $msgf_path -s $mzml -d ${target_db} -o $target_file $msgf_options

    decoy_file=${msgf_folder}/$base-decoy.mzid
    echo -e "\nCommand: java -Xmx2500M -jar $msgf_path -s $mzml -d ${decoy_db} -o $decoy_file $msgf_options"
    java -Xmx2500M -jar $msgf_path -s $mzml -d ${decoy_db} -o $decoy_file $msgf_options
  done
  echo -e "\n---- DONE\n"
}


apply_percolator()
{
  # percolator
  perc_folder=${out_dir}/percolator
  for d in ${perc_folder} ${perc_folder}/pin ${perc_folder}/xml ${perc_folder}/tab; do
    if ! [ -d $d ]; then
      mkdir $d
    fi
  done

  echo -e "\n---- Percolator"
  for target_mzid in ${out_dir}/msgf/*-target.mzid
  do
    base=`basename ${target_mzid} -target.mzid`    
    decoy_mzid=${out_dir}/msgf/$base-decoy.mzid
    echo -e "\n--Processing $base ..."
      
    msgfpin=${perc_folder}/pin/$base.pin 
    echo "Command: ${perc_install}/msgf2pin -M -o $msgfpin $target_mzid $decoy_mzid"
    ${perc_install}/msgf2pin -M -o $msgfpin $target_mzid $decoy_mzid
      
    xml_file=${perc_folder}/xml/$base.xml
    tab_file=${perc_folder}/tab/$base.tab
    echo -e "\nCommand: ${perc_install}/percolator -Z -A -X $xml_file $msgfpin" 
    ${perc_install}/percolator -Z -A -X $xml_file $msgfpin > $tab_file
  done
  echo -e "\n---- DONE\n"   
}   


### MAIN
#print_args
#apply_msgf
apply_percolator


