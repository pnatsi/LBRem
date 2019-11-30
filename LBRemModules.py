import statistics

def getNodesToRemove(input_tree, input_threshold):
    
    branch_lengths = [nodes.dist for nodes in input_tree.traverse('preorder')]
    shortest_bl = min(i for i in branch_lengths if i !=0)
    
    long_branches_leaves = []

    for node in input_tree.traverse('preorder'):
        if node.dist == shortest_bl:
            new_root_taxa=node.get_leaf_names()    
            if len(new_root_taxa) > 1:
                new_root_node=node.get_common_ancestor(new_root_taxa)
                input_tree.set_outgroup(new_root_node)
            else:
                input_tree.set_outgroup(new_root_taxa[0])
            
            branch_lengths_rooted = [node.dist for node in input_tree.traverse('preorder')]
            mean_bl_rooted = statistics.mean(branch_lengths_rooted)
            sd_bl_rooted = statistics.stdev(branch_lengths_rooted)
            threshold_rooted = (sd_bl_rooted * input_threshold)+ mean_bl_rooted
                
            for node in input_tree.traverse('preorder'):
                if node.dist > threshold_rooted:
                    leaves = node.get_leaf_names()
                    if len(leaves) < 0.5 * len(input_tree.get_leaf_names()):
                        long_branches_leaves.append(leaves)

    long_branches = [j for i in long_branches_leaves for j in i]
    long_branches_final = list(set(long_branches))
    
    return long_branches_final



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

