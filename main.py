import argparse
from parse_data import read_data
from statistics import *
from heal_scenarios import *
import multiprocessing
'\nID =  | Name =  | Description = '

# parsing of the line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Analystics and statistics options and XML file\'s path'
            '\nID = 00 | Name = Pre-condition not empty | Description = Scenario(s) without other scenario(s) in the pre-conditions '
            '\nID = 01 | Name = Triggers not empty | Description = Scenario(s) without other scenario(s) in the triggers.'
            '\nID = 02 | Name = Description not empty | Description = Scenario(s) without other scenario(s) in the description.'
            '\nID = 03 | Name = Post-condition not empty | Description = Scenario(s) without other scenario(s) in the post-conditions.'
            '\nID = 04 | Name = References not empty | Description = Scenario(s) without other scenario(s) in the references.'
            '\nID = 05 | Name = Link Pre-Condition to Post-Condition | Description = If S1 has S2 in Pre-conditions then S2 should have S1 in Post-conditions. S2->S1.'
            '\nID = 06 | Name = Link Trigger to Description | Description = If S1 has S2 in Triggers S2 then S2 should have S1 in Description. S2->S1.'
            '\nID = 07 | Name = Link Description to Trigger | Description = If S1 has S2 in Description then S2 should have S1 in Triggers. S1->S2.'
            '\nID = 08 | Name = Link Post-Condition to Pre-Condition | Description = If S1 has S2 in Post-conditions then S2 should have S1 in Pre-conditions. S1->S2.'
            '\nID = 09 | Name = Link References | Description = If S1 has S2 in References then:'
                                                 '\n\t\t\t- S1 should also have S2 mentioned in Pre-Conditions | Triggers | Description | Post-conditions.'
                                                 '\n\t\t\t- S2 should have S1 mentioned in Pre-Conditions | Triggers | Description | Post-conditions.'
            '\nID = 10 | Name = Longest path | Description = Find the longest path, like in the case of the graph.'
            '\nID = 11 | Name = Longest path containsscenario | Description = Find the longest path containing a specific scenario , like in the case of the graph.'
            '\nID = 12 | Name = Circular paths contains scenario | Description = Find all circular paths (the story never finish) , like in the case of the graph.'
            '\nID = 13 | Name = Circular paths contains scenario | Description = Find all circular paths (the story never finish) containing a specific scenario , like in the case of the graph.'
            '\nID = 14 | Name = The top of the most constly nodes | Description = Shows all the nodes that were called starting with the current node'
            ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-r', '--runOnScenario', type=str, metavar='', default='all', nargs='+',
                        help='Name of the scenario/scenarios the script will run the statistics and analytics on')
    parser.add_argument('-c', '--checkStatistic', type=int, metavar='', default=-1, nargs='+',
                        help='ID of the statistic/statistics')
    parser.add_argument('-i', '--ignore', action='store_true', help='Does not display the reading errors')
    parser.add_argument('-f', '--fileName', type=str, required=True, help='Path of the file')
    parser.add_argument('-rpp', '--reversePrecondPostcond', action='store_true', default=False,
                        help='Reverse precondition-postcondition arrow direction')
    parser.add_argument('-rtd', '--reverseTrigDesc', action='store_true', default=False,
                        help='Reverse trigger-description arrow direction')
    parser.add_argument('-t', '--top', type=int, metavar='', default=-1,
                        help='Top scenarios which consume the most resources')
    parser.add_argument('-hs', '--healScenarios', action='store_true', default=False,
                        help='Show statistics of the healed scenarios')
    parser.add_argument('-cpu', '--noCPU', type=int, metavar='', default=multiprocessing.cpu_count(),
                        help='Number of CPU used for multithreading')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Show log for the most time consuming statistics')

    args = parser.parse_args()

    return args


def print_stat_0_4_formatted(result, run_on_scenario, case):             # formatted display for statistics 0-4
    cont = 0
    print(case.upper())

    if run_on_scenario == 'all':
        for i in result:
            print('Nodes without {} {}'.format(case, i))
            cont = cont + 1
    else:
        intersection = list()
        result_upper = [x.upper() for x in result]
        for j in run_on_scenario:
            #j = j.upper()
            if j.upper() in result_upper:
                print('Nodes without {} {}'.format(case, j))
                cont = cont + 1
                #intersection.append(j)
        #print('Nodes without {} {}'.format(case, intersection))

    print("Results found: {}".format(str(cont)))
    print()


def print_stat_5_8_formatted(result, case, run_on_scenario):
    has_printed = False
    print(case.upper())
    cont = 0

    if run_on_scenario == 'all':
        for i in result.items():
            for j in i[1]:
                print('Broken {} from {} to {}'.format(case, j, i[0]))
                cont = cont + 1
            has_printed = True
    else:
        result_upper_keys = [x.upper() for x in result.keys()]
        run_on_scenario = list(run_on_scenario)
        for j in run_on_scenario:
            # j = j.upper()
            if j.upper() in result_upper_keys:
                for k in result[j]:
                    print('Broken {} from {} to {}'.format(case, k, j))
                    cont = cont + 1
                has_printed = True

    print("Results found: {}".format(str(cont)))
    if has_printed:
        print()


def print_stat_9_formatted(invalid_references_self, invalid_references_to_others, run_on_scenario):
    print('REFERENCES')
    has_printed = False
    cont = 0

    if run_on_scenario == 'all':
        # for each found, we display each value found
        for i in invalid_references_self.items():
            for reference in i[1]:
                print('Reference {} was not found in node {}\'s tags'.format(reference, i[0]))
                has_printed = True
                cont = cont + 1

        for i in invalid_references_to_others.items():
            for value in i[1]:
                print('In node {}, reference {} was found in {}, but node {} was not found in {}\'s {}'.format(i[0], value[1], value[0], i[0], value[1], value[2]))
                has_printed = True
                cont = cont + 1
    else:
        for i in invalid_references_self.items():
            if i[0] in run_on_scenario:
                for reference in i[1]:
                    print('Reference {} was not found in node {}\'s tags'.format(reference, i[0]))
                    has_printed = True
                    cont = cont + 1

        for i in invalid_references_to_others.items():
            if i[0] in run_on_scenario:
                for value in i[1]:
                    print('In node {}, reference {} was found in {}, but node {} was not found in {}\'s {}'.format(i[0], value[1], value[0], i[0], value[1], value[2]))
                    has_printed = True
                    cont = cont + 1

    print("Results found: {}".format(str(cont)))
    if has_printed:
        print()


def print_stat_10_formatted(results):
    print('LONGEST PATHS')

    for i in results:
        print(str(i)[1:-1])

    print("Results found: {}\n".format(len(results)))


def print_stat_11_formatted(results, run_on_scenario):
    print('LONGEST PATHS CONTAINING CERTAIN SCENARIOS')
    cont = 0

    if run_on_scenario == 'all':
        for i in results:
            print(str(i)[1:-1])
            cont = cont + 1
    else:
        for path in results:
            path_upper = [x.upper() for x in path]
            for scenario in run_on_scenario:
                if scenario.upper() in path_upper:
                    print("Scenario {} is found in path: {}".format(scenario, str(path)[1:-1]))
                    cont = cont + 1

    print("Results found: {}\n".format(str(cont)))


def print_stat_12_formatted(results):
    print('CYCLES')

    for i in results:
        print(str(i)[1:-1])

    print("Cycles found: {}\n".format(len(results)))


def print_stat_13_formatted(results, run_on_scenario):
    print('CYCLES CONTAINING CERTAIN SCENARIOS')
    cont = 0

    if run_on_scenario == 'all':
        for i in results:
            print(str(i)[1:-1])
            cont = cont + 1
    else:
        for path in results:
            path_upper = [x.upper() for x in path]
            for scenario in run_on_scenario:
                if scenario.upper() in path_upper:
                    print("Scenario {} is found in cycle: {}".format(scenario, str(path)[1:-1]))
                    cont = cont + 1

    print("Results found: {}\n".format(str(cont)))


def print_stat_14_formatted(results, top):
    cont = 0

    top_values = list(set(results.values()))      # set containing the unique values
    top_values.sort(reverse=True)

    result_tuples = list()
    for item in results.items():
        result_tuples.append((item[0], item[1]))
    result_tuples.sort(reverse=True, key=lambda t: t[1])    # sorting touple list descending, by value

    j = 0
    result_len = len(result_tuples)
    if top > len(top_values) or top < 1:
        top = len(top_values)
    print('TOP {} MOST CONSUMING SCENARIOS'.format(top))

    for i in range(top):
        while j < result_len and result_tuples[j][1] == top_values[i]:
            print('{}: {}'.format(result_tuples[j][0], result_tuples[j][1]))
            j = j + 1
            cont = cont + 1

    print('Result printed {}'.format(cont))


def check_options(options, nodes, run_on_scenario, pre_post, trig_desc, top, noCPU, heal, verbose):
    if options == -1:
        # SA SCHIMBI LA CATE OPTIUNI AI MAXIM + 1
        # IF YOU ADD MORE STATISTICS, YOU MUST INCREASE THE LIMIT BY HOW MANY STATISTICS YOU ADDED
        options = set(range(0, 15))         # if there is no requirements regarding the options, the program will display all of them
    else:
        options = set(options)

    if run_on_scenario != 'all':
        run_on_scenario = set(run_on_scenario)

    if noCPU < 1 or noCPU > multiprocessing.cpu_count():
        noCPU = multiprocessing.cpu_count()

    # statistics from 5 to 9 and 0 are mandatory for data cleaning, so we save the result and print it if necessary
    rez_stat_00 = stat_00(nodes)

    rez_stat_01 = stat_01(nodes)

    if heal:
        nodes = stat_05_heal(nodes)
        nodes = stat_06_heal(nodes)
        nodes = stat_07_heal(nodes)
        nodes = stat_08_heal(nodes)

    rez_stat_05 = stat_05(nodes)
    rez_stat_06 = stat_06(nodes)
    rez_stat_07 = stat_07(nodes)
    rez_stat_08 = stat_08(nodes)
    rez_stat_09 = stat_09(nodes)

    #print(nodes['J65'])
    #print(nodes['J64'])
    #print(nodes['J67'])

    default_roots = set(rez_stat_00).intersection(rez_stat_01)
    rez_stat_12 = stat_12(nodes, default_roots, pre_post, trig_desc, noCPU, verbose)        # we run stat 12 first, because we need to know the cycles for stat 10
    rez_stat_10 = stat_10(nodes, default_roots, pre_post, trig_desc)
    #rez_stat_12 = stat_12(nodes, set(rez_stat_00).intersection(rez_stat_01), pre_post, trig_desc)
    rez_stat_14 = stat_14(nodes, pre_post, trig_desc)

    for i in options:
        if i == 0:
            print_stat_0_4_formatted(rez_stat_00, run_on_scenario, 'preconditions')
        elif i == 1:
            print_stat_0_4_formatted(stat_01(nodes), run_on_scenario, 'triggers')
        elif i == 2:
            print_stat_0_4_formatted(stat_02(nodes), run_on_scenario, 'description')
        elif i == 3:
            print_stat_0_4_formatted(stat_03(nodes), run_on_scenario, 'postconditions')
        elif i == 4:
            print_stat_0_4_formatted(stat_04(nodes), run_on_scenario, 'references')
        elif i == 5:
            #print(stat_05(nodes))
            print_stat_5_8_formatted(rez_stat_05, 'precondition to postcondition link', run_on_scenario)
        elif i == 6:
            #print(stat_06(nodes))
            print_stat_5_8_formatted(rez_stat_06, 'trigger to description link', run_on_scenario)
        elif i == 7:
            #print(stat_07(nodes))
            print_stat_5_8_formatted(rez_stat_07, 'description to trigger link', run_on_scenario)
        elif i == 8:
            #print(stat_08(nodes))
            print_stat_5_8_formatted(rez_stat_08, 'postcondition to precondition link', run_on_scenario)
        elif i == 9:
            invalid_references_self, invalid_references_to_others = rez_stat_09
            print_stat_9_formatted(invalid_references_self, invalid_references_to_others, run_on_scenario)
        elif i == 10:
            print_stat_10_formatted(rez_stat_10)
        elif i == 11:
            print_stat_11_formatted(rez_stat_10, run_on_scenario)
        elif i == 12:
            print_stat_12_formatted(rez_stat_12)
        elif i == 13:
            print_stat_13_formatted(rez_stat_12, run_on_scenario)
        elif i == 14:
            print_stat_14_formatted(rez_stat_14, top)
        else:
            print('Option does not exist')


def main():
    args = parse_args()
    if args.runOnScenario != 'all':                                 # all scenarios will be transformed to upper case, because names are case insensitive
        args.runOnScenario = list(set(args.runOnScenario))
        args.runOnScenario = [i.upper() for i in args.runOnScenario]

    if args.checkStatistic != -1:
        args.checkStatistic = list(set(args.checkStatistic))

    nodes = read_data(args.fileName, args.ignore)
    check_options(args.checkStatistic, nodes, args.runOnScenario, args.reversePrecondPostcond, args.reverseTrigDesc,
                  args.top, args.noCPU, args.healScenarios, args.verbose)

if __name__ == '__main__':
    main()

# de pus descrieri


































