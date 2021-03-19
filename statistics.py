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
    invalid_references = dict()

    for node in nodes.items():
        new_references = list()
        for reference in node[1].get_references():
            if not ((reference in node[1].get_preconditions() and node[0] in nodes[reference].get_postconditions()) or \
                (reference in node[1].get_postconditions() and node[0] in nodes[reference].get_preconditions()) or \
                (reference in node[1].get_triggers() and node[0] in nodes[reference].get_description()) or \
                (reference in node[1].get_description() and node[0] in nodes[reference].get_triggers())):

                if node[0] not in invalid_references.keys():
                    invalid_references[node[0]] = [reference]
                else:
                    invalid_references[node[0]].append(reference)
            else:
                new_references.append(reference)
        node[1].set_references(new_references)

    return invalid_references
