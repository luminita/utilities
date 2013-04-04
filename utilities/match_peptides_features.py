import sys 
import data_handling.kronik as kronik 
import data_handling.other as other
import data_handling.percolator as percolator 
import data_handling.elude as elude
import data_structures.interval_tree as interval_tree
import ms_utilities.peptide_utilities as peptide_utilities
    

class PercolatorMatchedPeptide(percolator.PercolatorPeptide):
    def __init__(self, perc_id, svm_score, qvalue, pep, sequence, \
            proteins, is_decoy, retention_time, theoretical_mass, \
            matched_features, mass_interval):
        self.retention_time = float(retention_time)
        self.theoretical_mass = float(theoretical_mass)
        self.matched_features = matched_features
        self.mass_interval = mass_interval
        super(PercolatorMatchedPeptide, self).__init__(perc_id, svm_score, qvalue,\
            pep, sequence, proteins, is_decoy)                    
    
    def get_begin(self):
        return self.mass_interval[0]
        
    def get_end(self):
        return self.mass_interval[1]
  
    def __eq__(self, other):
        return self.sequence == other.sequence and \
                self.retention_time == other.retention_time      
        
    def __str__(self):
        to_str = super(PercolatorMatchedPeptide, self).__str__()
        to_str += ":::{}:::{}:::{}".format(self.theoretical_mass, \
                self.retention_time, self.mass_interval) 
        for feat in self.matched_features:
            to_str += ":::" + str(feat)
        return to_str
    
                    
def remove_duplicates(list_):
    unique = []
    for item in list_:
        if not item in unique:  
            unique.append(item)
    return unique  
  
          
def get_matched_peptides(percolator_peptides, rt_dict, mass_tolerance, \
        ptm_masses, verbosity):
    peptides = []
    for p in percolator_peptides:
        if p.sequence in rt_dict:
            rt = rt_dict[p.sequence]         
            theoretical_mass = peptide_utilities.PeptideUtilities().\
                    compute_monoisotopic_mass_without_charge(p.sequence, \
                    ptm_masses)
            offset = mass_tolerance*theoretical_mass*1e-6
            mass_interval = (theoretical_mass-offset, theoretical_mass+offset)
            peptides.append(PercolatorMatchedPeptide(p.perc_id, p.svm_score, \
                    p.qvalue, p.pep, p.sequence, p.proteins, p.is_decoy, \
                    rt, theoretical_mass, [], mass_interval))
        elif verbosity > 1:
            print "Warning: No retention time for {}".format(p.sequence)
    return peptides 
    
          
def match_peptides2features(percolator_tab_file, rt_file, kronik_file, \
        ptm_file=None, check_charge=True, mass_tolerance=5, \
        rt_tolerance=0.25, verbosity=2):            
    if check_charge:
        are_matching = lambda p, feat: \
                    p.retention_time >= feat.first_rt-rt_tolerance and \
                    p.retention_time <= feat.last_rt+rt_tolerance and \
                    feat.charge == int(p.perc_id.split("_")[-2])
    else:
        are_matching = lambda p, feat: \
                    p.retention_time >= feat.first_rt-rt_tolerance and \
                    p.retention_time <= feat.last_rt+rt_tolerance 
    # load data 
    percolator_peptides, percolator_proteins = percolator.PercolatorIO().\
            load_tab(percolator_tab_file, dot_notation=False, \
            verbosity=verbosity) 
    rt_dict = elude.EludeIO().load_rt_file(rt_file, verbosity=verbosity)        
    ms1_features = kronik.KronikIO().load_kronik_file(kronik_file, \
            verbosity=verbosity)
    ptms = other.load_ptm_file(ptm_file, verbosity=verbosity)
    
    # fill intervals and rts 
    peptides = get_matched_peptides(percolator_peptides, rt_dict, \
            mass_tolerance, ptms, verbosity=verbosity) 
    # build the interval tree (mass intervals)
    if verbosity > 2:
        print "\nBuilding interval tree ..."
    T = interval_tree.IntervalTree(peptides)
    if verbosity > 2:
        print "Done."           
    # perform the matching    
    if verbosity > 2:
        print "\nCompute matches..."        
    for feat in ms1_features:
        matching_mass = T.search(feat.monoisotopic_mass)
        if len(matching_mass) > 0:
            umatching_mass = remove_duplicates(matching_mass)
            matching_mass_rt = [p for p in umatching_mass if \
                    are_matching(p, feat)]            
            for peptide in matching_mass_rt:
                peptide.matched_features.append(feat)                     
    print "Done."   
    if verbosity > 2:
        print_summary(peptides)    
    return peptides    
    
    
def write_to_file(peptides, output_file, verbosity=2):
    if verbosity > 2:
        print "\nWrite output to {}".format(output_file)        
    outf = open(output_file, "w")
    outf.write("Peptide(PSMId,score,q-value,posterior_error_prob,")
    outf.write("peptide,proteinIds:::Theoretical mass:::Retention time:::")
    outf.write("Mass interval:::MS1-features(kronik lines)\n")
    for p in peptides:
        outf.write(str(p) + "\n")
    outf.close()
    if verbosity > 2:
        print "{} peptide written".format(len(peptides))        
    

def get_pair(str_pair):
    tmp = str_pair.replace("(", "").replace(")", "")
    values = tmp.split(",")
    return (float(values[0]), float(values[1]))


def load_peptides_matched(filename, verbosity=2):
    if verbosity > 2:
        print "\nLoading peptides from {}".format(filename)        
    lines = open(filename).readlines()[1:]
    peptides = []
    for l in lines:
        columns = l.split(":::")
        perc_cols = columns[0].split("\t")
        proteins = [p.strip() for p in perc_cols[5:]]
        theoretical_mass = columns[1]
        retention_time = columns[2]
        mass_interval = get_pair(columns[3])
        if len(columns) > 3:
            matched_features = [kronik.MS1Feature(["-"]+l.strip().split("\t")) \
                    for l in columns[4:]]        
        else:
            matched_features = []
        peptides.append(PercolatorMatchedPeptide(perc_cols[0], perc_cols[1], \
                perc_cols[2], perc_cols[3], perc_cols[4], proteins, \
                False, retention_time, theoretical_mass, matched_features, \
                mass_interval)) 
    if verbosity > 2:
        print "{} peptides were loaded".format(len(peptides))    
    return peptides
        

def print_summary(peptides):
    n_total = len(peptides)
    not_matched = len([p for p in peptides if len(p.matched_features)==0])
    n_unique_matched = len([p for p in peptides if len(p.matched_features)==1])
    n_multiply_matched = len([p for p in peptides if len(p.matched_features)>1])
    print "\n--------------------------"
    print "Total peptides:{}\nNot matched={}({}%)\nUniquely matched={}({}%)\nMultiply matched={}({}%)".\
            format(n_total, not_matched, not_matched/float(n_total)*100, \
            n_unique_matched, n_unique_matched/float(n_total)*100, \
            n_multiply_matched, n_multiply_matched/float(n_total)*100)
    print "--------------------------"    

    
def main():
    rt_file="data/20110429_Velos4_MaZe_SA_HeLaH-PrESTsL4-q0.01-rt.txt"
    tab_file="data/20110429_Velos4_MaZe_SA_HeLaH-PrESTsL4.percolator-q0.01.tab"
    kronik_file="data/20110429_Velos4_MaZe_SA_HeLaH-PrESTsL4.kronik"
    ptm_file = "data/ptms.txt"
    
    peptides = match_peptides2features(tab_file, rt_file, kronik_file, \
            ptm_file, mass_tolerance=5, rt_tolerance=0.1, verbosity=3)
    print_summary(peptides)
    write_to_file(peptides, "tmp/out.txt", verbosity=2)    
    my_peptides = load_peptides_matched("tmp/out.txt", verbosity=3)
    print_summary(my_peptides)
    write_to_file(my_peptides, "tmp/out2.txt", verbosity=2)
    


if __name__ == '__main__':
    main()
    
    
