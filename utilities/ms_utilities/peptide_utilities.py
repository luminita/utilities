'''
@ Created by Luminita Moruz 
March 7th, 2013
'''
from constants import MONOISOTOPIC_MASSES, MONOISOTOPIC_MASS_WATER, MASS_PROTON, MASS_CO, MASS_AMMONIA


class PeptideUtilities:
    @staticmethod
    def get_sequence(peptide_sequence):
        if peptide_sequence.find(".") != -1:
            return peptide_sequence.split(".")[1]            
        return peptide_sequence
        
        
    @staticmethod
    def compute_monoisotopic_mass_without_charge(peptide_sequence, ptm_masses={}):
        '''
        Compute the monoisotopic mass M of a peptide without charge 
        A dictionary with ptm_masses should be given 
        Example: {"K[UNIMOD:259]":8.014199+128.0949557, 
                  "R[UNIMOD:267]":10.008269+156.1011021}
        '''
        peptide = PeptideUtilities.get_sequence(peptide_sequence)
        # compute the mass 
        mm = 0.0
        modifs = ptm_masses.keys()
        for mod in modifs:
            while peptide.find(mod) != -1:
                mm += ptm_masses[mod]
                peptide = peptide.replace(mod, "", 1) 
        for i in range(len(peptide)):
            mm += MONOISOTOPIC_MASSES[ord(peptide[i]) - ord('A')]
        return (mm + MONOISOTOPIC_MASS_WATER)


    @staticmethod    
    def compute_monoisotopic_mass_with_charge(peptide_sequence):
        '''
        Compute the monoisotopic mass of a peptide including the
        charge (one proton)
        '''
        mm = PeptideUtilities.compute_monoisotopic_mass_without_charge(\
                peptide_sequence) 
        return (mm + MASS_PROTON)
        
    
    @staticmethod    
    def get_b_y_ions(peptide_sequence):
        '''
        Given a peptide sequence, get the list of b and y ions singly charged 
        Note that the results is [b1, .., bn-1], [yn-1, .., y1]        
        '''
        peptide = PeptideUtilities.get_sequence(peptide_sequence)
        b = []
        total_mass = 0.0
        n = len(peptide)
        for i in range(n):
            total_mass += MONOISOTOPIC_MASSES[ord(peptide[i])-ord('A')]
            b.append(total_mass + MASS_PROTON)  
        # 2*MASS_PROTON is used to calculate y ions properly
        total_mass += MONOISOTOPIC_MASS_WATER + 2*MASS_PROTON                
        y = [total_mass-MASS_PROTON] + [total_mass-bi for bi in b[:-1]] 
        return b, y
        
    
    @staticmethod    
    def get_all_ions(peptide_sequence):
        '''
        Given a sequence, return:
        - [b1, .., bn-1] singly charged
        - [yn-1, ..., y1] singly charged
        - [yn-1, ..., y1] doubly charged
        - [a1, .., an-1] ions 
        '''
        b, y = PeptideUtilities.get_b_y_ions(peptide_sequence)
        a, b0, b_star, b_doubly_charged = zip(*[(bi-MASS_CO, bi-MONOISOTOPIC_MASS_WATER, \
                bi-MASS_AMMONIA, (bi+MASS_PROTON)/2) for bi in b])
        y_doubly_charged, y0, y_star = zip(*[((yi+MASS_PROTON)/2, \
                yi-MONOISOTOPIC_MASS_WATER, yi-MASS_AMMONIA) for yi in y])
        return b, y, a, b0, b_star, b_doubly_charged, y_doubly_charged, y0, y_star
        
        
def main():            
    #b, y = PeptideUtilities.get_b_y_ions("LIEDNEYTAR")
    b, y, a, b0, b_star, y_doubly_charged, y0, y_star = PeptideUtilities.get_all_ions("TFTGCWTCR")
    #for (s, n) in zip([b, y, a, b0, b_star, y_doubly_charged, y0, y_star], \
    #        ['b','y','a','b0','b*','y++','y0','y*']):
    #    print "\n", n, ": ", s, "\n"
    x = b + y + list(a) + list(b0) +list(b_star) + list(y_doubly_charged) + list(y0) + list(y_star) 
    x.sort()
    for z in x:
        print z
    
    

if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
        
        
