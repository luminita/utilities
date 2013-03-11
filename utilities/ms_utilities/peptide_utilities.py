'''
@ Created by Luminita Moruz 
March 7th, 2013
'''

class PeptideUtilities:
    @staticmethod
    def compute_monoisotopic_mass_without_charge(peptide_sequence):
        '''
        Compute the monoisotopic mass M of a peptide without charge 
        '''
        monoisotopic_masses = [71.0371103, 0.0, 160.0306443, 115.0269385, \
                129.0425877, 147.0684087, 57.0214611, 137.0589059, \
                113.0840579, 0.0, 128.0949557, 113.0840579, 131.0404787, \
                114.0429222, 0.0, 97.0527595, 128.0585714, 156.1011021, \
                87.0320244, 101.0476736, 0.0, 99.0684087, 186.0793065, \
                0.0, 163.0633228, 0.0]
        monoisotopic_mass_water = 18.0105633 
        # check if the peptide is given in the format X.Y.Z
        peptide = peptide_sequence
        if peptide_sequence.find(".") != -1:
            peptide = peptide_sequence.split(".")[1]            
        # compute the mass 
        mm = 0.0
        for i in range(len(peptide)):
            mm += monoisotopic_masses[ord(peptide[i]) - ord('A')]
        return (mm + monoisotopic_mass_water)

    @staticmethod    
    def compute_monoisotopic_mass_with_charge(peptide_sequence):
        '''
        Compute the monoisotopic mass of a peptide including the
        charge (one proton)
        '''
        mass_proton = 1.00727646677
        mm = PeptideUtilities.compute_monoisotopic_mass_without_charge(\
                peptide_sequence) 
        return (mm + mass_proton)


