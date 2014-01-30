'''
Small utilities to manipulate proteins
'''
import sys
sys.path.append("..")
import data_handling.other as other

def trypsin_digest_protein(sequence, min_len=7, max_len=40):
    '''
    Given a protein sequence sequence, perform a trypsin digestion and 
    return a list of the peptides longer than 7 
    Notes:
    - Trypsin cuts at K or R, except for when either is followed by P
    - The returned list may contain duplicates 
    '''
    peptides = []
    i = 0 
    while i < len(sequence):
        idx = i 
        while (idx < len(sequence)-1) and \
                (((sequence[idx]=='K' or sequence[idx]=='R') and \
                sequence[idx+1]=='P') or \
                (sequence[idx]!='K' and sequence[idx]!='R')):
            idx += 1
        pep = sequence[i:idx+1]
        len_pep = len(pep)
        if len_pep >= min_len and len_pep <= max_len:
            peptides.append(pep)
        i = idx + 1
    return peptides
        
    
def trypsin_digest(fasta_file, out_file, mappings_file=None, \
			min_len=7, max_len=40):
    '''
    Given a fasta file, perform an insilico digest of the proteins. The 
    list of theoretical peptides, one per line, are written to the out_file.
    If mappings_file is not None, then a file including a peptide and the 
    proteins to which this peptide is mapping is written
    Notes:
    - the order of the peptides in the output file is arbitrary
    '''    
    proteins = other.load_fasta_file(fasta_file, full_name=False, verbosity=3)
    all_peptides = {}
    for protein, sequence in proteins.iteritems():
        peptides = trypsin_digest_protein(sequence, min_len, max_len)
        for p in peptides:
            if p in all_peptides:
                all_peptides[p].append(protein)
            else:
                all_peptides[p] = [protein]
    # write the peptides to the output file
    other.write_list_to_file(sorted(all_peptides.keys()), out_file, verbosity=3)
    if mappings_file != None:
        to_write = ["{}\t{}".format(t[0], "\t".join(t[1])) \
                for t in all_peptides.items()]
        other.write_list_to_file(to_write, mappings_file, verbosity=3)				        
	


    
if __name__ == '__main__':
    sequence = "KKAAARRBBRRPCCKKPDDKEEEREEE"
    sequence = "KAAARRBBRRPCCKKPDDKEEEREEE"
    print sequence
    print trypsin_digest_protein(sequence, min_len=0, max_len=40)

    trypsin_digest("/scratch/lumi_work/projects/gradient_design/java/NonlinearGradientsUI/data/insilico/yeast.fasta", "/scratch/lumi_work/projects/gradient_design/java/NonlinearGradientsUI/data/insilico/Y", mappings_file=None, \
			min_len=8, max_len=50)
    
