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
        to_str = "{}\t{}\t{}".format(self.perc_id, self.pep)
        for peptide in self.peptides:
            to_str += "\t{}".format(peptide)
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
        proteins = {}
        i = 0
        while i<len(lines) and not lines[i].startswith("ProteinId"):
            columns = lines[i].split("\t")
            protein_ids = [col.strip() for col in columns[5:]]
            if dot_notation:
                seq = columns[4]
            elif columns[4].find(".") != -1:
                seq = columns[4].split(".")[1]
            peptide = PercolatorPeptide(columns[0], columns[1], \
                    columns[2], columns[3], seq, protein_ids, \
                    False)
            peptides.append(peptide)
            for prot in protein_ids:
                if prot in proteins:
                    proteins[prot].peptides.append(peptide) 
                else:
                    proteins[prot] = PercolatorProtein(prot, -1.0, -1.0, \
                            [peptide], False)
            i += 1
        # load the proteins 
        while i<len(lines):
            columns = lines[i].split()
            if columns[0] not in proteins and verbosity > 1:
                print "Warning: protein {} has no peptides identified;" + \
                        "it will be skipped".format(col[0])
            else:
                proteins[columns[0]].qvalue = columns[1]
                proteins[columns[0]].pep = columns[2]
            i += 1
        if verbosity > 2:
            print "{} peptides, {} proteins loaded".format(len(peptides), \
                    len(proteins))
        return peptides, proteins.values()
        
                
            
        
        
    
    
