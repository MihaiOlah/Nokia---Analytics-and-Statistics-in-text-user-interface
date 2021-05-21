# ===================================================================================================================
# it's the same algorithm from the statistics use for searching, except instead of returning a list with broken links
# we add the missing node in the other's fields so there is no longer a broken link
# ===================================================================================================================


def stat_05_heal(nodes):
    for node in nodes.items():                                                      # for each node in the main dictionary
        for precondition in node[1].get_preconditions():                            # we search for each precondition
            if node[0] not in nodes[precondition].get_postconditions():             # and we check if the current node apears in the postconditions of the node represented by the precondition
                nodes[precondition].add_postcondition(node[0])                      # we add the missing postcondition to the scenario missing it (the one in whose preconditions we are searching)

    return nodes


def stat_06_heal(nodes):
    for node in nodes.items():                                                      # for each node in the main dictionary
        for trigger in node[1].get_triggers():                                      # we search for each precondition
            if node[0] not in nodes[trigger].get_description():                     # and we check if the current node apears in the description of the node represented by the triggers
                nodes[trigger].add_description(node[0])                             # we add the missing description to the scenario missing it (the one in whose triggers we are searching)

    return nodes


def stat_07_heal(nodes):
    for node in nodes.items():                                                      # for each node in the main dictionary
        for description in node[1].get_description():                               # we search for each precondition
            if node[0] not in nodes[description].get_triggers():                    # and we check if the current node apears in the triggers of the node represented by the description
                nodes[description].add_trigger(node[0])                             # we add the missing trigger to the scenario missing it (the one in whose description we are searching)

    return nodes


def stat_08_heal(nodes):
    for node in nodes.items():                                                      # for each node in the main dictionary
        for postcondition in node[1].get_postconditions():                          # we search for each precondition
            if node[0] not in nodes[postcondition].get_preconditions():             # and we check if the current node apears in the precondition of the node represented by the postconditions
                nodes[postcondition].add_precondition(node[0])                      # we add the missing preconditions to the scenario missing it (the one in whose postconditions we are searching)

    return nodes
