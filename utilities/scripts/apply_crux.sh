#!/bin/bash
# Command line arguments:
# - folder including the ms2 files 
# - target fasta file (if the index is already created, should be in the same dir with extension .index)
# - decoy fasta file (if the index is already created, should be in the same dir with extension .index)
# - crux executable 
# - file including the parameters of the search 
# - directory including the output files 

# Notes: the index differs from one version of crux to another! 

# Command line arguments 
ms2_dir=$1
target_db=$2
decoy_db=$3
crux_path=$4
crux_params=$5
out_dir=$6
##########

# print the command line arguments 
echo -e "\n------------------------------------"
echo "Command line arguments:"
echo -e "------------------------------------"    
echo "ms2_dir=${ms2_dir}"
echo "target_db=${target_db}"
echo "decoy_db=${decoy_db}"
echo "crux_path=${crux_path}"
echo "crux_params_file=${crux_params}"
echo "out_dir=${out_dir}"
echo -e "------------------------------------"

# create the output directory if it doesnt exist 
if ! [ -d ${out_dir} ]; then
  mkdir ${out_dir}
fi    

# create an index for each database (I check only the target here)
if [ -d ${target_db}.index ]; then
  echo "-------- Index exists"
else
  echo "-------- Creating index ..."
  $crux_path create-index --overwrite T --parameter-file $crux_params $target_db ${target_db}.index
  $crux_path create-index --overwrite T --parameter-file $crux_params $decoy_db ${decoy_db}.index
  echo "-------- DONE."
fi

for ms2 in ${ms2_dir}/*.ms2
do
  tmp=${ms2%%.ms2}
  base=${tmp##*/}
  echo "-------- Processing $base ..."
  # remove previous searches
  if [ -d $out_dir/$base ]; then
    rm -r $out_dir/$base
  fi
  mkdir $out_dir/$base
  mkdir $out_dir/$base/target
  mkdir $out_dir/$base/decoy
  
  # run crux with target
  echo "-------- Running crux for target: $crux_path sequest-search --output-dir $out_dir/$base/target --overwrite T --parameter-file $crux_params $ms2 ${target_db}.index"
  $crux_path sequest-search --output-dir $out_dir/$base/target --overwrite T --parameter-file $crux_params $ms2 ${target_db}.index
  
  # run crux with decoy
  echo "-------- Running crux for decoy: $crux_path sequest-search --output-dir $out_dir/$base/decoy --overwrite T --parameter-file $crux_params $ms2 ${decoy_db}.index"
  $crux_path sequest-search --output-dir $out_dir/$base/decoy --overwrite T --parameter-file $crux_params $ms2 ${decoy_db}.index
  echo "-------- DONE."  
done
