"""
Given a file in the format (Note it is not the percolator format):
PSM	qvalue	score	PEP	Peptide	Proteins

a fileroot, and an output folder, then format the data in the output 
required by FIDO and run FIDO. 
"""
import sys 
import os 


def get_fido_files(input_file, fileroot, out_folder):
    print "\n Generating input files ..."
    graph_filename = os.path.join(out_folder, fileroot + "-graph-fido.txt") 
    outf_gf = open(graph_filename, "w")
    lines = open(input_file).readlines()[1:]
    all_proteins = set([])
    for l in lines:
        fields = l.split()
        pep = float(fields[3])
        seq = fields[4].split(".")[1]
        proteins = [p.strip() for p in fields[5:]]
        
        outf_gf.write("e {}\n".format(seq))
        for p in proteins:
            outf_gf.write("r {}\n".format(p))
        outf_gf.write("p {}\n".format(1.0 - pep))
        all_proteins = all_proteins.union(set(proteins))
    outf_gf.close()
    
    target_proteins = [p for p in all_proteins if p.startswith("present") or p.startswith("absent")]
    decoy_proteins = [p for p in all_proteins if p.startswith("decoy")]
    print "Test {} + {} = {} = {}".format(len(target_proteins), \
            len(decoy_proteins), len(target_proteins) + len(decoy_proteins), \
            len(all_proteins))
            
    td_filename = os.path.join(out_folder, fileroot + "-td-fido.txt")
    outf_td = open(td_filename, "w")
    for prot_li in [target_proteins, decoy_proteins]:    
        outf_td.write("{")
        outf_td.write(" {}".format(prot_li[0]))
        for t in prot_li[1:]:
            outf_td.write(" , {}".format(t))            
        outf_td.write(" }\n")    
    outf_td.close()

    print "\nDone."
    return graph_filename, td_filename
    
 
def run_fido(fido_path, graph_filename, td_filename, fileroot, out_folder):
    fido_file = os.path.join(out_folder, fileroot + "-fido.out")
    err_file = os.path.join(out_folder, fileroot + "-fido.err")
    command = "{} {} {} > {} 2> {}".format(fido_path, graph_filename, \
            td_filename, fido_file, err_file)
    print "\n Running {}".format(command)
    os.system(command)
    print "\nDone."
    return fido_file
    

def format_output(fido_out_file, fileroot, out_folder):
    print "\nFormatting .."
    #0.9988 { gi|1574458|gb|AAC23247 }
    #0.6788 { SW:TRP6_HUMAN , GP:AJ271067_1 , GP:AJ271068_1 }
    lines = [l for l in open(fido_out_file).readlines() if l.find("{") != -1]
    pairs = []
    all_proteins = []
    for l in lines:
        prob = float(l.split("{")[0])
        proteins = [p.strip() for p in l.split("{")[1].replace("}", "").split(",")]
        all_proteins += proteins 
        for p in proteins:
            pairs.append((p, prob))

    if len(all_proteins) != len(set(all_proteins)):
        print "WARNING: non unique proteins in the file"
            
    pairs.sort(key = lambda p: p[1], reverse = True)
    outfile = os.path.join(out_folder, fileroot + "-fido-proteins.txt")
    outf = open(outfile, "w")
    outf.write("Protein\tFido-probability\n")
    for p in pairs:
        outf.write("{}\t{}\n".format(p[0], p[1]))    
    outf.close()
    print "{} proteins were written to the output".format(len(pairs))
    print "{} proteins with prob > 0.99".format(len([p for p in pairs if p[1] > 0.99]))

def main():
    # the fido path should include the options 
    fido_path = sys.argv[1]
    input_file = sys.argv[2]
    fileroot = sys.argv[3]
    out_folder = sys.argv[4]
    
    graph_filename, td_filename = get_fido_files(input_file, fileroot, \
            out_folder)            
    fido_file = run_fido(fido_path, graph_filename, td_filename, \
            fileroot, out_folder)
    format_output(fido_file, fileroot, out_folder)       
    

if __name__ == '__main__':
    main()
    
    
