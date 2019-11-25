from ete3 import Tree
import LBRemModules as lbrm
import argparse


usage = "A script to remove long branches."
toolname = "LBRem"
footer = "Who \n Mattia Giacomelli (mattia.giacomelli@bristol.ac.uk); \n Paschalis Natsidis (p.natsidis@ucl.ac.uk); \n \nWhere \n Pisani Lab, Uni Bristol; \n Telford Lab, UCL;\n\
 ITN IGNITE; \n  \nWhen\n November 2019; \n\n"

parser = argparse.ArgumentParser(description = usage, prog = toolname, epilog = footer, formatter_class=argparse.RawDescriptionHelpFormatter,)
parser.add_argument('-f', metavar = 'filename', dest = 'fasta_file', required = True,
                    help = 'full path to fastas file')
parser.add_argument('-t', metavar = 'filename', dest = 'trees_file', required = True,
                    help = 'full path to trees file')
parser.add_argument('-sd', metavar = 'int', dest = 'sd', required = True,
                    help = 'How many standard deviations a branch length must deviate from the mean in order to get removed')
parser.add_argument('-w', metavar = 'directory', dest = 'working_dir', required = True,
                    help = 'full path to working directory')

#parser.print_help()

args = parser.parse_args()

#READ USER INPUT
fasta_input = args.fasta_file
trees_input = args.trees_file
standard_deviations = int(args.sd)
wdir = args.working_dir

fastas_txt_file = open(fasta_input, "r")
trees_txt_file = open(trees_input, "r")

fastas_lines = fastas_txt_file.readlines()
trees_lines = trees_txt_file.readlines()

fastas = [x.strip() for x in fastas_lines]
trees = [x.strip() for x in trees_lines]

for i in range(len(fastas)):
    
    current_tree = Tree(wdir + trees[i])
    current_fasta = wdir + fastas[i]
    
    long_branches = lbrm.getNodesToRemove(current_tree, standard_deviations)    # GET THE BRANCHES THAT ARE LONGER THAN THE SET THRESHOLD
    
    lbrm.RemoveSequences(current_tree,  current_fasta, long_branches)           # WRITE THE NEW FASTAS WITHOUT THE SEQUENCES OF THE LONG BRANCHES

