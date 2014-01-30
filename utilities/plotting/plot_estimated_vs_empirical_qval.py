""" Given a file including 
Protein	PEP	q-value

or 

Fido-probability	Protein

plot the estimated vs empirical qvalue. The file is assumed to have the first line as 
header. 

The qvalues are estimated as follows:
- the estimated qvalues is calculated by sorting the PEP, then traversing 
the list and averaging the PEPs (decoys are removed)
- the empirical qvalue is calculated by sorting the PEPs, then traversing 
the list and calculating for each target the #target/#decoys encountered so farc"""

import sys 
import matplotlib.pyplot as plt
import operator

class Protein:
    def __init__(self, protein_name, pep):
        self.name = protein_name
        self.pep = pep
        if protein_name.startswith("random"):
            self.is_decoy = True
        else:
            self.is_decoy = False
        self.est_q = -1.0
        self.emp_q = -1.0
   
    def __repr__(self):
        return "{} {} ".format(self.name, self.pep)
   

def load_protein_probabilities(protein_file):
    #Load the protein probabilities from the input file
    #return a list of pairs (PEP, protein_name) """
    print "\nLoading {}".format(protein_file)
    proteins = []
    for l in open(protein_file).readlines()[1:]:
        fields = l.split()
        if len(fields) > 2:
            proteins.append(Protein(fields[0].strip(), float(fields[1])))
        else:
            proteins.append(Protein(fields[1].strip(), 1.0-float(fields[0])))
    print "{} proteins were loaded. ".format(len(proteins))
    return proteins
    
    
def compute_empirical_qval(proteins):
    proteins.sort(key = operator.attrgetter('pep'))
    
    for x in proteins:
        print x
    idx_target = 0.0
    idx_decoy = 0.0
    for prot in proteins:
        if prot.is_decoy:
            idx_decoy += 1.0
        else:
            idx_target += 1.0
            prot.emp_q = idx_decoy / idx_target      
            
                    
def compute_estimated_qval(proteins):
    proteins.sort(key = operator.attrgetter('pep'))
    sum_pep = 0.0
    i = 0
    for prot in proteins:
        if not prot.is_decoy:
            sum_pep += prot.pep
            i += 1
            prot.est_q = sum_pep / i
       

def plot_qvalues(proteins, out_file):
    """ plot empirical vs estimated qvalues """    
    plt.plot([p.emp_q for p in proteins if not p.is_decoy], \
             [p.est_q for p in proteins if not p.is_decoy], "ro", \
             markeredgewidth = 0.0, markeredgecolor ="red", markersize = 3.0 )
    plt.xscale('log')
    plt.yscale('log')
    plt.plot([1e-3, 1], [1e-3, 1], "k-")    
    plt.plot([1e-3, 1], [2e-3, 2], "k--")    
    plt.plot([1e-3, 1], [0.5e-3, 0.5], "k--")            
    plt.xlim([1e-3, 1])
    plt.ylim([1e-3, 1])
    plt.ylabel("Estimated q value", fontsize = 20)
    plt.xlabel("Empirical q value", fontsize = 20)
    plt.savefig(out_file + ".png", format = "png")
    

def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    
    proteins = load_protein_probabilities(infile)
    compute_empirical_qval(proteins)
    compute_estimated_qval(proteins)
    plot_qvalues(proteins, outfile)
    

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
