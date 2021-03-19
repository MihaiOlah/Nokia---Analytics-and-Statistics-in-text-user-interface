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
    args = parser.parse_args()

    return args

def print_stat_0_4_formatted(result, run_on_scenario, case):             # formatted display for statistics 0-4
    if run_on_scenario == 'all':
        print('Nodes without {} {}'.format(case, result))
    else:
        intersection = list()
        for j in run_on_scenario:
            #j = j.upper()
            if j in result:
                intersection.append(j)
        print('Nodes without {} {}'.format(case, intersection))
    print()

def print_stat_5_8_formatted(result, case, run_on_scenario):
    has_printed = False
    print(case.upper())
    if run_on_scenario == 'all':
        for i in result.items():
            for j in i[1]:
                print('Broken {} from {} to {}'.format(case, j, i[0]))
            has_printed = True
    else:
        for j in run_on_scenario:
            #j = j.upper()
            if j in result.keys():
                for k in result[j]:
                    print('Broken {} from {} to {}'.format(case, k, j))
                has_printed = True

    if has_printed:
        print()

def print_stat_9_formatted(invalid_references_self, invalid_references_to_others, run_on_scenario):
    print('REFERENCES')
    has_printed = False

    if run_on_scenario == 'all':
        # for each found, we display each value found
        for i in invalid_references_self.items():
            for reference in i[1]:
                print('Reference {} was not found in node {}\'s tags'.format(reference, i[0]))
                has_printed = True

        for i in invalid_references_to_others.items():
            for value in i[1]:
                print('In node {}, reference {} was found in {}, but node {} was not found in {}\'s {}'.format(i[0], value[1], value[0], i[0], value[1], value[2]))
                has_printed = True
    else:
        for i in invalid_references_self.items():
            if i[0] in run_on_scenario:
                for reference in i[1]:
                    print('Reference {} was not found in node {}\'s tags'.format(reference, i[0]))
                    has_printed = True

        for i in invalid_references_to_others.items():
            if i[0] in run_on_scenario:
                for value in i[1]:
                    print('In node {}, reference {} was found in {}, but node {} was not found in {}\'s {}'.format(i[0], value[1], value[0], i[0], value[1], value[2]))
                    has_printed = True
    if has_printed:
        print()

def check_options(options, nodes, run_on_scenario):
    if options == -1:
        # SA SCHIMBI LA CATE OPTIUNI AI MAXIM + 1
        options = set(range(0, 10))         # if there is no requirements regarding the options, the program will display all of them
    else:
        options = set(options)

    if run_on_scenario != 'all':
        run_on_scenario = set(run_on_scenario)

    for i in options:
        if i == 0:
            print_stat_0_4_formatted(stat_00(nodes), run_on_scenario, 'preconditions')
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
            print_stat_5_8_formatted(stat_05(nodes), 'precondition to postcondition link', run_on_scenario)
        elif i == 6:
            #print(stat_06(nodes))
            print_stat_5_8_formatted(stat_06(nodes), 'trigger to description link', run_on_scenario)
        elif i == 7:
            #print(stat_07(nodes))
            print_stat_5_8_formatted(stat_07(nodes), 'description to trigger link', run_on_scenario)
        elif i == 8:
            #print(stat_08(nodes))
            print_stat_5_8_formatted(stat_08(nodes), 'postcondition to precondition link', run_on_scenario)
        elif i == 9:
            invalid_references_self, invalid_references_to_others = stat_09(nodes)
            print_stat_9_formatted(invalid_references_self, invalid_references_to_others, run_on_scenario)
        else:
            print('Option does not exist')

def main():
    args = parse_args()
    if args.runOnScenario != 'all':                                 # all scenarios will be transformed to upper case, because names are case insensitive
        args.runOnScenario = [i.upper() for i in args.runOnScenario]
    nodes = read_data(args.fileName, args.ignore)
    check_options(args.checkStatistic, nodes, args.runOnScenario)

if __name__ == '__main__':
    main()