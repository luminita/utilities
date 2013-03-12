
class EludeIO:
    @staticmethod
    def load_rt_file(filename, dot_notation=False, verbosity=2):   
        if verbosity > 2:
            print "\nLoading {}".format(filename)
        lines = open(filename).readlines()
        peptides = {}
        for l in lines:
            columns = l.split()
            if dot_notation:
                seq = columns[0]
            elif columns[0].find(".") != -1:
                seq = columns[0].split(".")[1]
            peptides[seq] = float(columns[1])
        if verbosity > 2:
            print "{} peptides were loaded.".format(len(peptides))        
        return peptides 
            
        
        
        
