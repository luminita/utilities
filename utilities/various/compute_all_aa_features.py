# @ Created by L. Moruz, 1.03.2011
# given a dataset peptide, retention time (or some other target value), and a number of features 
# computes many other features and outputs them in csv format 
import sys 

class Peptide: 
  def __init__(self, given_sequence, sequence, target, old_features):
    self.given_sequence = given_sequence
    self.sequence = sequence
    self.target = target
    self.old_features = old_features 
    self.new_features = []
    
  def __str__(self):
    return self.sequence + " " + str(self.old_features) + " " + str(self.new_features) + \
           " " + str(self.target)
      
# load a file and return a map with the key amino acid, and the value an unique index
# and a list of peptides;
# all peptides with less than min_residues or more than max_residues are removed 
def LoadFile(filename, min_residues, max_residues):
  print "\nLoad file "  + filename + "..."
  
  inf = open(filename, "r")
  lines = inf.readlines()
  inf.close()
    
  amino_acids = {}
  peptides = []
  index = 0
  for l in lines[2:]:
    fields = l.split()
    if fields[0].find(".") != -1:
      sequence = fields[0].split(".")[1]
    else:
      sequence = fields[0]
    n = len(sequence)
    if n >= min_residues and n <= max_residues:
      for aa in list(sequence):
        if aa not in amino_acids:
          amino_acids[aa] = index
          index += 1
      old_features = [float(fields[i]) for i in range(2,len(fields))]
      peptides.append(Peptide(fields[0], sequence, float(fields[1]), old_features))

  #for p in peptides:
  # print str(p)
  print str(len(peptides)) + " peptides were loaded"
  return amino_acids, peptides 

# given an index and a size, return a list of including 0 everywhere except for index 
def FillWithZeros(index, size):
  l = [0 for i in range(size)]
  l[index] = 1
  
  return l

# given map amino_acid, index, a number of positions, and a peptide
# compute a feature for each position peptide (number_positions x number of amino_acids)
def ComputePositionFeaturesPeptide(amino_acids, number_positions, peptide):
  #print "Compute features..."
  no_amino_acids = len(amino_acids)
  peptide_aa = list(peptide.sequence)

  features_left = []
  features_right = []  
  start_index = 0
  end_index = len(peptide_aa) - 1
  while start_index < end_index:
    index_start_aa = amino_acids[peptide_aa[start_index]]
    features_left += FillWithZeros(index_start_aa, no_amino_acids)
    index_end_aa = amino_acids[peptide_aa[end_index]]
    features_right = FillWithZeros(index_end_aa, no_amino_acids) + features_right
    start_index += 1
    end_index -= 1
  if start_index == end_index:
    index_start_aa = amino_acids[peptide_aa[start_index]]
    features_left += FillWithZeros(index_start_aa, no_amino_acids)
   
  no_features = len(amino_acids) * number_positions
  no_features_middle = no_features - (len(features_left) + len(features_right))
  middle_features = [0 for i in range(no_features_middle)]
  
  peptide.new_features = [float(f) for f in features_left + middle_features + features_right]
  
  #print str(len(peptide.features)) + " were computed"
  return peptide  

# write a list of peptides in Csv format 
# first write the old features, and then the new ones 
def WriteCSVFile(peptides, filename):
  outf = open(filename, "w")
  print "\nWriting peptides to " + filename + " ..."

  for pep in peptides:
    outf.write(pep.given_sequence)
    for f in pep.old_features:
      outf.write("," + str(f))
    for f in pep.new_features:
      outf.write("," + str(f))
    outf.write("," + str(pep.target) + "\n")
  print str(len(peptides)) + " were written"
  outf.close()  

def ComputeOtherFeatures(peptide):
  # square cube of old features 
  for f in peptide.old_features:
    peptide.new_features.append(f*f)
  for f in peptide.old_features:
    peptide.new_features.append(f*f*f)
  # add the product of each feature with all the others 
  for i in range(len(peptide.old_features) - 1):
    for j in range(i + 1, len(peptide.old_features)):
      peptide.new_features.append(peptide.old_features[i] * peptide.old_features[j])
  # add the sum of each feature with all the others 
  for i in range(len(peptide.old_features) - 1):
    for j in range(i + 1, len(peptide.old_features)):
      peptide.new_features.append(peptide.old_features[i] + peptide.old_features[j])


def ComputeAdditionalFeatures(amino_acids, number_positions, peptide):
  pep = ComputePositionFeaturesPeptide(amino_acids, number_positions, peptide)
  final_peptide = ComputeOtherFeatures(pep)

  return pep

# Main function to compute features 
def ComputeFeatures(in_filename, min_residues, max_residues, out_filename):
  amino_acids, peptides = LoadFile(in_filename, min_residues, max_residues)
  
  print "\nCompute additional features..."
  processed_peptides = []
  for p in peptides:
    processed_peptides.append(ComputeAdditionalFeatures(amino_acids, max_residues, p))
  print str(len(peptides[0].new_features)) + " new features were computed"
  print "Total number of features: " + str(len(peptides[0].new_features) + len(peptides[0].old_features))
  
  WriteCSVFile(processed_peptides, out_filename)
  
def main():
  if sys.argv[1] == "help":
    print """
    This script computes the features of a group of peptides 
    Command line arguments: 
    1. Input file (peptide sequence, pi per line, space separated) 
    2. Min peptide length 
    3. Max peptide length 
    4. Out file (csv format)
    """
    return 
 
  in_file = sys.argv[1]
  min_len = int(sys.argv[2]) 
  max_len = int(sys.argv[3])
  out_file = sys.argv[4]
  ComputeFeatures(in_file, min_len, max_len, out_file)
  #lengths = [len(l.split()[0].split(".")[1]) for l in open(in_file, "r").readlines()[2:]]
  #print min(lengths), max(lengths)

  
if __name__ == '__main__':
  main()
    
