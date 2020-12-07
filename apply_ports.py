#!/usr/bin/env python3.8

import argparse
import sys

from more_itertools import flatten, consecutive_groups

from more_itertools import consecutive_groups


def list_to_set(ports:list):
    """
    Converts a list of lists into a set, containing all numbers between each min and max value
    :param ports: list of ports to convert
    :type ports: list[list]
    :return: set of ports
    :rtype: set
    """
    result = set()
    for port in ports:
        for num in range(port[0], port[1]+1):
            result.add(num)
    return result


def group(ports):
    """
    Groups numbers that are consecutive and then reduces them to the min and max for each group
    :param ports: ports included
    :type ports: list
    :return: included ports in min-max format
    :rtype: list[list]
    """
    result = []
    grouped = [list(num) for num in consecutive_groups(ports)]
    for i in grouped:
        result.append([min(i), max(i)])
    result.sort()
    return result


def remove_irrelevant(include, exclude):
    not_used = set()
    for i in include:
        for j in exclude:
            if j[0] in range(i[0], i[1] + 1):
                pass
            if j[1] in range(i[0], i[1] + 1):
                pass
            else:
                not_used.add([j[0], j[1]])
    return not_used


def apply_port_exclusions(include_ports, exclude_ports):
    """
    Applies exclusions to a list of included ports.
    :param include_ports: ports to include
    :type include_ports: list[list]
    :param exclude_ports: ports to exclude
    :type exclude_ports: list[list]
    :return: modified list of included ports minus the excluded ports
    :rtype: list[list]
    """
    if len(include_ports) == 0:
        return []
    irrelevant = remove_irrelevant(include_ports, exclude_ports)
    include = list_to_set(include_ports)
    exclude = list_to_set(exclude_ports)
    # include.add(irrelevant)
    ports = include.symmetric_difference(exclude)
    portslist = list(ports)
    portslist.sort()
    result = group(portslist)
    return result


def validate_input(ports):
    """
    Validates that ports are in correct format
    :param ports: list of lists
    :type ports: list[list]
    :return: whether or not length is correct
    :rtype: bool
    """
    for i in ports:
        if len(i) == 2 or len(i) == 0:
            return True
        else:
            return False


def create_parser():
    """
    Create argument parser for command line use
    :return: Argument Parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('include_ports', help='ports to include')
    parser.add_argument('exclude_ports', help='ports to exclude')
    return parser


def main(args):
    """
    Main loop that houses all calls to various functions, runs program from start to finish
    """
    # Create parser with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into namespace called 'ns'
    ns = parser.parse_args(args)
    # if wrong input was given on command line, print the required parameters and exit
    if not ns:
        parser.print_usage()
        sys.exit()

    try:
        if validate_input(ns.include_ports) and validate_input(ns.exclude_ports):
            test = apply_port_exclusions(ns.include_ports, ns.exclude_ports)
            print("Output after applying exclusions: ")
            print(test)
    except ValueError:
        print("Invalid input")

if __name__ == '__main__':
    main(sys.argv[1:])


