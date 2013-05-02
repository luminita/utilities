#!/bin/bash
# Command line arguments:
# - folder including the mzml files (they need to have the extension .mzML)
# - target fasta file (if the index is already created, should be in the same dir with extension .index)
# - decoy fasta file (if the index is already created, should be in the same dir with extension .index)
# - msgf+ executable 
# - msgf+ options (important to include these within "")
# - directory including the output files 

# Command line arguments 
mzml_dir=$1
target_db=$2
decoy_db=$3
msgf_path=$4
msgf_options=$5
out_dir=$6
##########

# print the command line arguments 
echo -e "\n------------------------------------"
echo "Command line arguments:"
echo -e "------------------------------------"    
echo "mzml_dir=${mzml_dir}"
echo "target_db=${target_db}"
echo "decoy_db=${decoy_db}"
echo "msgf_path=${msgf_path}"
echo "msgf_options=${msgf_options}"
echo "out_dir=${out_dir}"
echo -e "------------------------------------"

# create the output directories if they dont exist
for d in ${out_dir} ${out_dir}/target ${out_dir}/decoy
do
  if ! [ -d $d ]; then
    mkdir $d
  fi
done

if ! [ -d ${out_dir} ]; then
  mkdir ${out_dir}
fi

for mzml in ${mzml_dir}/*.mzML
do
  base=`basename $mzml .mzML`
  echo "-------- Processing $base ..."

  target_file=${out_dir}/target/$base-target.mzid
  echo "Command: java -Xmx2500M -jar $msgf_path -s $mzml -d ${target_db} -o $target_file $msgf_options"
  java -Xmx2500M -jar $msgf_path -s $mzml -d ${target_db} -o ${target_file} ${msgf_options}

  decoy_file=${out_dir}/decoy/$base-decoy.mzid
  echo -e "\nCommand: java -Xmx2500M -jar $msgf_path -s $mzml -d ${decoy_db} -o $decoy_file $msgf_options"
  java -Xmx2500M -jar $msgf_path -s $mzml -d ${decoy_db} -o ${decoy_file} ${msgf_options}
  echo "-------- DONE."  
done
	
