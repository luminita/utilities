def load_ptm_file(filename, verbosity=2):
    '''
    Modification Mass
    K[UNIMOD:259]	136.1091547
    '''
    if verbosity > 2:
        print "\nLoading {}".format(filename)
    if filename != None:
        lines = open(filename).readlines()[1:]
        ptm_masses = dict([(l.split("\t")[0], float(l.split("\t")[1])) \
            for l in lines])        
    else:
        ptm_masses = {}
    if verbosity > 2:
        print "{} ptms loaded.".format(len(ptm_masses))
    return ptm_masses
    
    
def load_fasta_file(filename, full_name=False, verbosity=2):
    '''
    Load a fasta file and return a dictionary protein name -> sequence
    if full_name = true, then the name of the protein as given in the fasta 
    file is considered; otherwise, only the part until the first space
    '''
    if verbosity > 2:
        print "\nLoading {}".format(filename)    
    
    lines = open(filename).readlines()  
    i = 0
    proteins = {}
    get_protein_name = lambda full_name: full_name.split()[0]  
    while i < len(lines):
        if lines[i].startswith(">"):
            if full_name:
                protein_name = lines[i][1:].strip()
            else:
                protein_name = get_protein_name(lines[i][1:])                
            sequence = ""
            i += 1
            while i < len(lines) and not lines[i].startswith(">"):
                sequence += lines[i].strip()
                i += 1
            proteins[protein_name] = sequence
  
    if verbosity > 2:
        print "{} proteins loaded.".format(len(proteins))
      
    return proteins
    


def write_list_to_file(my_list, out_file, verbosity=2):
    '''
    Write a list of objects to out_file 
    '''
    if verbosity > 2:
        print "\nWriting to {}".format(out_file)        
	
    outf = open(out_file, "w")
    for l in my_list:
        outf.write("{}\n".format(l))
    outf.close()
	
    if verbosity > 2:
        print "{} lines were written".format(len(my_list))    
    
	
