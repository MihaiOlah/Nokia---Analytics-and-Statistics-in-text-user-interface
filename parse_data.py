import xml.etree.ElementTree as ET
from Node import *

#if a node appears more than once, the keep only the first occurrence
def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    nodes = dict()                                  #dictionary containg all nodes
    duplicates = dict()                             #dictionary containing all nodes' names that appear more than one time and how many times

    #node[0] -> name
    #node[1] -> link
    #node[2] -> preconditions
    #node[3] -> triggers
    #node[4] -> description
    #node[5] -> postconditions
    #node[6] -> references
    for node in root.findall("./node"):
        if node[0].text not in nodes.keys():        #if the node appears for the first time, we add it to the main dictionary
            nodes[node[0].text] = Node(node[0].text, node[1].text, [i.text for i in node[2]],
            [i.text for i in node[3]], [i.text for i in node[4]], [i.text for i in node[5]],
            [i.text for i in node[6]])
        elif node[0].text not in duplicates.keys(): #if the node appears the second time, we add it to the duplicates
            duplicates[node[0].text] = 2
        else:                                       #if the node appears more than two times, the number of appearances is updated
            duplicates[node[0].text] = duplicates.get(node[0].text) + 1


    #for i in nodes.values():
        #print('{}\n'.format(i))
    return nodes, duplicates

#clearing nonexisting nodes are those nodes for which there is no instance in "nodes"
def clear_non_existent_nodes(nodes):
    nonExistentNodes = set()                        #all nonexisting nodes' names
    nodes_names = nodes.keys()                      #list with the names of all existing nodes' names

    #searching in the fields of all existing nodes if there are names which are
    #missing from the list containing all existing ones and creating a new list only with the correct data
    for node in nodes.values():
        tmp = list()                            # new list containig only the existing nodes
        for i in node.get_preconditions():
            if i in nodes_names:                # if the node exists, it's added in the list, else it's added to the non-existent
                tmp.append(i)
            else:
                nonExistentNodes.add(i)
        node.set_preconditions(tmp)             # this will be the "clear" list, which will be passed as correct

        tmp = list()                            # new list containig only the existing nodes
        for i in node.get_triggers():
            if i in nodes_names:                # if the node exists, it's added in the list, else it's added to the non-existent
                tmp.append(i)
            else:
                nonExistentNodes.add(i)
        node.set_triggers(tmp)             # this will be the "clear" list, which will be passed as correct

        tmp = list()                            # new list containig only the existing nodes
        for i in node.get_description():
            if i in nodes_names:                # if the node exists, it's added in the list, else it's added to the non-existent
                tmp.append(i)
            else:
                nonExistentNodes.add(i)
        node.set_description(tmp)             # this will be the "clear" list, which will be passed as correct

        tmp = list()                            # new list containig only the existing nodes
        for i in node.get_postconditions():
            if i in nodes_names:                # if the node exists, it's added in the list, else it's added to the non-existent
                tmp.append(i)
            else:
                nonExistentNodes.add(i)
        node.set_postconditions(tmp)             # this will be the "clear" list, which will be passed as correct

        tmp = list()                            # new list containig only the existing nodes
        for i in node.get_references():
            if i in nodes_names:                # if the node exists, it's added in the list, else it's added to the non-existent
                tmp.append(i)
            else:
                nonExistentNodes.add(i)
        node.set_references(tmp)             # this will be the "clear" list, which will be passed as correct

    return nodes, nonExistentNodes

#if the tags contained parent's node name, the name is deleted from the respective tags
def node_name_in_own_tags(nodes):
    flagged_nodes = set()

    for node in nodes.values():
        found = False
        name = node.get_name()             #node name
        if name in node.get_preconditions():
            node.remove_preconditions(name)
            found = True
        if name in node.get_triggers():
            node.remove_triggers(name)
            found = True
        if name in node.get_description():
            node.remove_description(name)
            found = True
        if name in node.get_postconditions():
            node.remove_postconditions(name)
            found = True
        if name in node.get_references():
            node.remove_references(name)
            found = True
        if found:                          #if the tags contained parent's node name, we add it to the flagged nodes
            flagged_nodes.add(name)

    #for i in nodes:
        #print('{}\n'.format(i))

    return nodes, flagged_nodes

def read_data(path, *argv):
    #nodes, duplicates = parse_xml('C:\\Users\\Mihai\\Desktop\\Proiect\\date.xml')
    nodes, duplicates = parse_xml(path)
    nodes, nonExistentNodes = clear_non_existent_nodes(nodes)
    nodes, flagged_nodes = node_name_in_own_tags(nodes)

    #for i in nodes.values():
        #print('{}\n'.format(i))

    if argv[0] == False:                # check if ignore option (-i/--ignore) is enabled or not
        if bool(duplicates):            # check if dictionary is empty
            print("Duplicate nodes in file:")
            for i in duplicates.items():
                print("Node {} appears {} times\n".format(i[0], i[1]))

        if len(nonExistentNodes) != 0:  # check if set is empty
            print("Non-existent nodes in file that are referenced in existent nodes' tags:\n" + str(nonExistentNodes) + '\n')

        if len(flagged_nodes) != 0:     # check if set is empty
            print("Nodes being referenced in their own tags:\n" + str(flagged_nodes) + '\n')

    return nodes