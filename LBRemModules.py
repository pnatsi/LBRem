import statistics

def getNodesToRemove(input_tree, input_threshold):
    
    branch_lengths = [nodes.dist for nodes in input_tree.traverse('preorder')]
    mean_bl = statistics.mean(branch_lengths)
    std_bl = statistics.stdev(branch_lengths)
    threshold = std_bl*input_threshold + mean_bl
    
    long_branches_leaves = []

    for node in input_tree.traverse('preorder'):
        node.resolve_polytomy()
        if node.dist > threshold:
            leaves = node.get_leaf_names()
            if len(leaves) < 0.8 * len(input_tree.get_leaf_names()):
                long_branches_leaves.append(leaves)
    long_branches = [j for i in long_branches_leaves for j in i]

    return list(set(long_branches))


def RemoveSequences(input_tree, input_fasta, long_branches):
    
    with open(input_fasta, 'r') as fasta:  
        lines = fasta.readlines()
        stripped = [x.strip() for x in lines]
        
    long_branches_sorted = sorted(long_branches)
    
    output = open(input_fasta + ".new", "w+")
    for i in range(0, len(stripped), 2):   
        if stripped[i][1:] not in long_branches_sorted:
            output.write(stripped[i]+ "\n")
            output.write(stripped[i+1] + "\n")
