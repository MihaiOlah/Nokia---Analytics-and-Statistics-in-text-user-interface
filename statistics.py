paths = list()
cycles = list()
top_resources = dict()

def stat_00(nodes):
    withoutPreconditions = list()           # list containing the nodes without precondition

    for i in nodes.items():
        if len(i[1].get_preconditions()) == 0:
            withoutPreconditions.append(i[0])

    return withoutPreconditions

def stat_01(nodes):
    withoutTrigger = list()                     # list containing the nodes without triggers

    for i in nodes.items():
        if len(i[1].get_triggers()) == 0:
            withoutTrigger.append(i[0])

    return withoutTrigger

def stat_02(nodes):
    withoutDescription = list()                 # list containing the nodes without description

    for i in nodes.items():
        if len(i[1].get_description()) == 0:
            withoutDescription.append(i[0])

    return withoutDescription

def stat_03(nodes):
    withoutPostconditions = list()              # list containing the nodes without postconditions

    for i in nodes.items():
        if len(i[1].get_postconditions()) == 0:
            withoutPostconditions.append(i[0])

    return withoutPostconditions

def stat_04(nodes):
    withoutReferences = list()                  # list containing the nodes without references

    for i in nodes.items():
        if len(i[1].get_references()) == 0:
            withoutReferences.append(i[0])

    return withoutReferences

def stat_05(nodes):
    link_pre_post = dict()                      # dictionary containing the node as key and a list with all broken links as value

    for node in nodes.items():                                                      # for each node in the main dictionary
        new_preconditions = list()                                                  # list containg all valid links nodes from preconditions
        for precondition in node[1].get_preconditions():                            # we search for each precondition
            if node[0] not in nodes[precondition].get_postconditions():             # and we check if the current node apears in the postconditions of the node represented by the precondition
                if node[0] not in link_pre_post.keys():                             # if it's the first broken link coresponding to this node, we add it to the broken links dictionary
                    link_pre_post[node[0]] = [precondition]
                else:                                                               # else we add it to the rest of the broken links
                    link_pre_post[node[0]].append(precondition)
            else:                                                                   # if the node is found in the postconditions of the node reprezented by 'precondition', then it's a valid link
                new_preconditions.append(precondition)
        node[1].set_preconditions(new_preconditions)

    return link_pre_post

def stat_06(nodes):
    link_trig_desc = dict()                      # dictionary containing the node as key and a list with all broken links as value

    for node in nodes.items():                                                      # for each node in the main dictionary
        new_triggers = list()
        for trigger in node[1].get_triggers():                                      # we search for each precondition
            if node[0] not in nodes[trigger].get_description():                     # and we check if the current node apears in the postconditions of the node represented by the precondition
                if node[0] not in link_trig_desc.keys():                            # if it's the first broken link coresponding to this node, we add it to the broken links dictionary
                    link_trig_desc[node[0]] = [trigger]
                else:                                                               # else we add it to the rest of the broken links
                    link_trig_desc[node[0]].append(trigger)
            else:  # if the node is found in the postconditions of the node reprezented by 'precondition', then it's a valid link
                new_triggers.append(trigger)
            node[1].set_triggers(new_triggers)

    return link_trig_desc

def stat_07(nodes):
    link_desc_trig = dict()                      # dictionary containing the node as key and a list with all broken links as value

    for node in nodes.items():                                                              # for each node in the main dictionary
        new_description = list()
        for description in node[1].get_description():                                       # we search for each precondition
            if node[0] not in nodes[description].get_triggers():                            # and we check if the current node apears in the postconditions of the node represented by the precondition
                if node[0] not in link_desc_trig.keys():                                    # if it's the first broken link coresponding to this node, we add it to the broken links dictionary
                    link_desc_trig[node[0]] = [description]
                else:                                                                       # else we add it to the rest of the broken links
                    link_desc_trig[node[0]].append(description)
            else:                                                               # if the node is found in the postconditions of the node reprezented by 'precondition', then it's a valid link
                new_description.append(description)
            node[1].set_description(new_description)

    return link_desc_trig

def stat_08(nodes):
    link_post_pre = dict()                      # dictionary containing the node as key and a list with all broken links as value

    for node in nodes.items():                                                      # for each node in the main dictionary
        new_postconditions = list()
        for postcondition in node[1].get_postconditions():                            # we search for each precondition
            if node[0] not in nodes[postcondition].get_preconditions():             # and we check if the current node apears in the postconditions of the node represented by the precondition
                if node[0] not in link_post_pre.keys():                             # if it's the first broken link coresponding to this node, we add it to the broken links dictionary
                    link_post_pre[node[0]] = [postcondition]
                else:                                                               # else we add it to the rest of the broken links
                    link_post_pre[node[0]].append(postcondition)
            else:                                                           # if the node is found in the postconditions of the node reprezented by 'precondition', then it's a valid link
                new_postconditions.append(postcondition)
            node[1].set_postconditions(new_postconditions)

    return link_post_pre

def stat_09(nodes):
    invalid_references_self = dict()                # reference not appearing in node's fields
    invalid_references_to_others = dict()           # references' origin node not found in other nodes' tags

    # for each node we check if the references appear in node's tags and if they appear
    # we search if the node appears in one of the logically correct tags
    # (eg if reference appears in node's preconditions, the node must appear in references' postconditions)
    for node in nodes.items():
        new_references = list()
        for reference in node[1].get_references():
            if (reference not in node[1].get_preconditions()) and (reference not in node[1].get_triggers()) \
                                 and (reference not in node[1].get_description()) and (reference not in node[1].get_postconditions()):   # checking if the reference does not appear in node's tags
                if node[0] not in invalid_references_self.keys():
                    invalid_references_self[node[0]] = [reference]
                else:
                    invalid_references_self[node[0]].append(reference)
            # checking if the node is found in other's tags
            elif (reference in node[1].get_preconditions()) and (node[0] not in nodes[reference].get_postconditions()):
                if node[0] not in invalid_references_to_others.keys():
                    invalid_references_to_others[node[0]] = [('preconditions', reference, 'postconditions')]
                else:
                    invalid_references_to_others[node[0]].append(('preconditions', reference, 'postconditions'))
            elif (reference in node[1].get_postconditions()) and (node[0] not in nodes[reference].get_preconditions()):
                if node[0] not in invalid_references_to_others.keys():
                    invalid_references_to_others[node[0]] = [('postconditions', reference, 'preconditions')]
                else:
                    invalid_references_to_others[node[0]].append(('postconditions', reference, 'preconditions'))
            elif (reference in node[1].get_triggers()) and (node[0] not in nodes[reference].get_description()):
                if node[0] not in invalid_references_to_others.keys():
                    invalid_references_to_others[node[0]] = [('triggers', reference, 'description')]        # triplet containg data for display
                else:
                    invalid_references_to_others[node[0]].append(('triggers', reference, 'description'))
            elif (reference in node[1].get_description()) and (node[0] not in nodes[reference].get_triggers()):
                if node[0] not in invalid_references_to_others.keys():
                    invalid_references_to_others[node[0]] = [('description', reference, 'triggers')]
                else:
                    invalid_references_to_others[node[0]].append(('description', reference, 'triggers'))
            else:
                new_references.append(reference)
        node[1].set_references(new_references)

    return invalid_references_self, invalid_references_to_others

# in depth graph traversal and backtracking for finding all paths
# the paths are added to the global variable "paths"
# each time a longer path is found, the content of "paths" is deleted and the new longest path is added
# if there are multiple path, then they are added among the rest of the longest paths
def scenario_traversal(nodes, root, pre_post, trig_desc, path = []):
    global paths

    if root not in path:

        path.append(root)

        if not pre_post and not trig_desc:      # default directions
            neighbours = nodes[root].get_postconditions() + nodes[root].get_description()
        elif pre_post and not trig_desc:        # reverse precond-postcond direction
            neighbours = nodes[root].get_preconditions() + nodes[root].get_description()
        elif not pre_post and trig_desc:        # reverse trigger-description direction
            neighbours = nodes[root].get_postconditions() + nodes[root].get_triggers()
        else:                                   # reverse both direction
            neighbours = nodes[root].get_preconditions() + nodes[root].get_triggers()

        for neighbour in neighbours:
            path = scenario_traversal(nodes, neighbour, pre_post, trig_desc, path)
        else:
            if len(paths) > 0:
                if len(paths[0]) < len(path):
                    paths = list()
                    paths.append(list(path))
                elif len(paths[0]) == len(path):
                    paths.append(list(path))
            else:
                paths.append(list(path))

            if len(path) > 0 and root in path:
                path.pop()

    if len(paths) > 0:
        if len(paths[0]) < len(path):
            paths = list()
            paths.append(list(path))
        elif len(paths[0]) == len(path):
            paths.append(list(path))
    else:
        paths.append(list(path))

    return path

def stat_10(nodes, root_nodes, pre_post, trig_desc):
    global paths

    for root in root_nodes:
        scenario_traversal(nodes, root, pre_post, trig_desc)

    return paths

# checking if the current cycle already exists in "cycles" by checking if it's a rotated form of another
def cycle_is_rotated(cycle):
    global cycles

    same = False
    len_cycle = len(cycle) - 1
    for tmp_cycle in cycles:
        if len(tmp_cycle) == len(cycle) and tmp_cycle[0] in cycle:
            j = cycle.index(tmp_cycle[0])  # index in cycle to be added
            for i in range(len(tmp_cycle) - 1):      # not counting the last element which is equal with the first; i index in tem_cycle
                if tmp_cycle[i] != cycle[:-1][j]:
                    break
                j = (j + 1) % len_cycle
            else:
                same = True
        if same:
            break

    if not same:
        cycles.append(cycle)


# in depth graph traversal and backtracking for finding all paths
# the paths are added to the global variable "paths"
# each time a longer path is found, the content of "paths" is deleted and the new longest path is added
# if there are multiple path, then they are added among the rest of the longest paths
def scenario_traversal_cycle(nodes, root, pre_post, trig_desc, cycle = []):
    global cycles

    if root not in cycle:

        cycle.append(root)

        if not pre_post and not trig_desc:      # default directions
            neighbours = nodes[root].get_postconditions() + nodes[root].get_description()
        elif pre_post and not trig_desc:        # reverse precond-postcond direction
            neighbours = nodes[root].get_preconditions() + nodes[root].get_description()
        elif not pre_post and trig_desc:        # reverse trigger-description direction
            neighbours = nodes[root].get_postconditions() + nodes[root].get_triggers()
        else:                                   # reverse both direction
            neighbours = nodes[root].get_preconditions() + nodes[root].get_triggers()

        for neighbour in neighbours:
            cycle = scenario_traversal_cycle(nodes, neighbour, pre_post, trig_desc, cycle)
        else:
        #    if len(paths) > 0:
         #       if len(paths[0]) < len(cycle):
          #          paths = list()
           #         paths.append(list(cycle))
            #    elif len(paths[0]) == len(cycle):
             #       paths.append(list(cycle))
           # else:
            #cycles.append(list(cycle))

            #if len(cycle) > 0 and root in cycle:
            cycle.pop()

    else:
        #print(cycle.index(root))
        #cycle.append(root)
        tmp = cycle[cycle.index(root):]     # isolating the cycle from the entire path
        tmp.append(root)                    # adding the last node to close the cycle
        cycle_is_rotated(tmp)
        #cycles.append(tmp)
        #print(cycle)
        #cycle.pop()
        """"
        if root == cycle[0]:
            cycle.append(root)

            #if len(cycles) > 0:
             #   if len(cycles[0]) < len(cycle):
              #      cycles = list()
               #     cycles.append(list(cycle))
               # elif len(cycles[0]) == len(cycle):
                #    cycles.append(list(cycle))
            #else:
            cycles.append(list(cycle))
            cycle.pop()
        else:
            cycle.append(root)
            print(cycle)
            cycle.pop()
            return cycle
        """
    return cycle

def remove_cycles(nodes, cycles):
    for cycle in cycles:
        for node_index in range(len(cycle) - 1):
            cur_node = cycle[node_index]
            next_node = cycle[node_index + 1]

            if next_node in nodes[cur_node].get_postconditions():
                nodes[cur_node].remove_postconditions(next_node)
                nodes[next_node].remove_preconditions(cur_node)
            elif next_node in nodes[cur_node].get_description():                           # if next node it's not in postconditions, then it's in description
                nodes[cur_node].remove_description(next_node)
                nodes[next_node].remove_triggers(cur_node)

    return nodes

def stat_12(nodes, root_nodes, pre_post, trig_desc):
    global cycles

    for root in root_nodes:
        scenario_traversal_cycle(nodes, root, pre_post, trig_desc)
    #print(cycles)
    return cycles

# if a scenario is leaf, it costs 1 to be executed
# if a scenario is not leaf, it costs 1 (value of itself) + sum of the values of the children scenarios
def stat_14(nodes, pre_post, trig_desc):
    global top_resources
    global cycles

    nodes_copy = dict(nodes)
    nodes_copy = remove_cycles(nodes_copy, cycles)

    not_leaves_nodes = list()
    leaves_nodes = set(stat_02(nodes_copy)).intersection(stat_03(nodes_copy))   # set containing leaves scenarios
    for leaf in leaves_nodes:       # each leaf consts 1, because it's only the value of itself
        top_resources[leaf] = 1

    for node in nodes_copy.keys():          # finding not leaf nodes
        if node not in leaves_nodes:
            not_leaves_nodes.append(node)
    if len(leaves_nodes) > 0:
        while len(not_leaves_nodes) > 0:
            not_visited = list()
            for node in not_leaves_nodes:
                children = nodes_copy[node].get_postconditions() + nodes_copy[node].get_description()
                sum_value = 0
                for child in children:
                    if child not in top_resources:
                        not_visited.append(node)
                        break
                    else:       # calculating the value for all children
                        sum_value = sum_value + top_resources[child]
                else:
                    top_resources[node] = sum_value + 1     # sum of children + itself
            not_leaves_nodes = not_visited
            print(not_leaves_nodes)

    return top_resources



