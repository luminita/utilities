class Peptide(object):
    '''
    Class to store a peptide
    '''
    def __init__(self, sequence, is_decoy):
        self.sequence = sequence
        self.is_decoy = bool(is_decoy)
    
    
class PercolatorPeptide(Peptide):
    '''
    Class to store information from percolator about a peptide 
    '''
    def __init__(self, perc_id, svm_score, qvalue, pep, sequence, \
            proteins, is_decoy):
        super(PercolatorPeptide, self).__init__(sequence, is_decoy)
        self.perc_id = perc_id
        self.svm_score = float(svm_score)
        self.qvalue = float(qvalue)
        self.pep = float(pep)
        self.proteins = proteins        
         
    def __str__(self):
        to_str = "{}\t{}\t{}\t{}\t{}".format(self.perc_id, \
                self.svm_score, self.qvalue, self.pep, self.sequence)
        for prot in self.proteins:
            to_str += "\t{}".format(prot)
        return to_str
        

class PercolatorProtein:
    '''
    Class to store information from percolator about a protein 
    '''
    def __init__(self, perc_id, qvalue, pep, peptides, is_decoy):
        self.perc_id = perc_id
        self.qvalue = float(qvalue)
        self.pep = float(pep)
        # list of PercolatorPeptide objects
        self.peptides = peptides 
        self.is_decoy = bool(is_decoy)
        
    def __str__(self):
        to_str = "{}\t{}\t{}".format(self.perc_id, self.qvalue, self.pep)
        to_str += "\n-------\n"
        for peptide in self.peptides:
            to_str += "\t{}\n".format(peptide)
        return to_str

        
class PercolatorIO:
    @staticmethod
    def load_tab(filename, dot_notation=False, verbosity=2):         
        '''
        Columns in input file (tab separated):
        PSMId	score	q-value	posterior_error_prob	peptide	proteinIds
        followed by:
        ProteinId	q-value	posterior_error_prob	peptideIds
        @Return a list of PercolatorPeptide objects, and a list of 
        PercolatorProtein objects  
        '''
        if verbosity > 2:
            print "Loading {}".format(filename)
        lines = open(filename).readlines()[1:]
        peptides = []
        i = 0
        while i<len(lines) and not lines[i].startswith("ProteinId"):
            columns = lines[i].split("\t")
            protein_ids = [col.strip() for col in columns[5:]]
            if dot_notation or columns[4].find(".") == -1:
                seq = columns[4]
            else:
                seq = columns[4].split(".")[1]
            peptide = PercolatorPeptide(columns[0], columns[1], \
                    columns[2], columns[3], seq, protein_ids, \
                    False)
            peptides.append(peptide)
            i += 1
        i += 1
        # load the proteins         
        proteins = []
        while i<len(lines):
            columns = lines[i].split()
            peps = [c.strip() for c in columns[3:]]
            proteins.append(PercolatorProtein(columns[0], columns[1], \
                    columns[2], peps, False))
            i += 1
        if verbosity > 2:
            print "{} peptides, {} proteins loaded".format(len(peptides), \
                    len(proteins))
        return peptides, proteins
        
                
            
        
        
    
    
