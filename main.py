import argparse
from parse_data import read_data
from statistics import *

# parsing of the line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Analystics and statistics options and XML file\'s path')
    parser.add_argument('-r', '--runOnScenario', type=str, metavar='', default='all', nargs='+',
                        help='Name of the scenario/scenarios the script will run the statistics and analytics on')
    parser.add_argument('-c', '--checkStatistic', type=int, metavar='', default=-1, nargs='+',
                        help='ID of the statistic/statistics')
    parser.add_argument('-i', '--ignore', action='store_true', help='Does not display the reading errors')
    parser.add_argument('-f', '--fileName', type=str, required=True, help='Path of the file')
    parser.add_argument('-rpp', '--reversePrecondPostcond', action='store_true', default=False, help='Reverse precondition-postcondition arrow direction')
    parser.add_argument('-rtd', '--reverseTrigDesc', action='store_true', default=False, help='Reverse trigger-description arrow direction')
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

    print("Results found: {}".format(len(results)))

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

    print("Results found: {}".format(str(cont)))

def print_stat_12_formatted(results):
    print('CYCLES')

    for i in results:
        print(str(i)[1:-1])

    print("Cycles found: {}".format(len(results)))

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

    print("Results found: {}".format(str(cont)))

def check_options(options, nodes, run_on_scenario, pre_post, trig_desc):
    if options == -1:
        # SA SCHIMBI LA CATE OPTIUNI AI MAXIM + 1
        options = set(range(0, 14))         # if there is no requirements regarding the options, the program will display all of them
    else:
        options = set(options)

    if run_on_scenario != 'all':
        run_on_scenario = set(run_on_scenario)

    # statistics from 5 to 9 and 0 are mandatory for data cleaning, so we save the result and print it if necessary
    rez_stat_00 = stat_00(nodes)
    rez_stat_05 = stat_05(nodes)
    rez_stat_06 = stat_06(nodes)
    rez_stat_07 = stat_07(nodes)
    rez_stat_08 = stat_08(nodes)
    rez_stat_09 = stat_09(nodes)
    rez_stat_10 = stat_10(nodes, rez_stat_00, pre_post, trig_desc)
    rez_stat_12 = stat_12(nodes, rez_stat_00, pre_post, trig_desc)

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
    check_options(args.checkStatistic, nodes, args.runOnScenario, args.reversePrecondPostcond, args.reverseTrigDesc)

if __name__ == '__main__':
    main()



































