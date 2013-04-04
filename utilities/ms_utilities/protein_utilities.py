'''
Small utilities to manipulate proteins
'''


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
        
    
if __name__ == '__main__':
    sequence = "KKAAARRBBRRPCCKKPDDKEEEREEE"
    print sequence
    print trypsin_digest_protein(sequence, min_len=0, max_len=40)
    
    
