#!/usr/bin/env python3.8

from more_itertools import flatten
import argparse
import sys


def combine_overlap(port1, port2):
    if port1[0] <= port2[0] <= port2[1] <= port1[1]:
        return port1
    if port2[0] <= port1[0] <= port1[1] <= port2[1]:
        return port2
    if port1[0] <= port2[0] <= port1[1] <= port2[1]:
        return [port1[0], port2[1]]
    if port2[0] <= port1[0] <= port2[1] <= port1[1]:
        return [port2[0], port1[1]]


def group(portlist):
    plist = [i for i in flatten(portlist)]
    result = []
    a = b = plist[0]
    for i in plist[1:]:
        if i == b+1:
            b = i
        else:
            result.append(a if a == b else [a, b])
            a = b = i
    result.append(a if a == b else [a, b])
    return result


# def merge(exclude_ports):
#     exclude_ports.sort()
#     for i in range(len(exclude_ports)):
#         # if exclude_ports[i][0] < exclude_ports[i + 1][0] < exclude_ports[i + 1][1] < exclude_ports[i][1]:
#             return exclude_ports[i]
#     return exclude_ports


def remove_doubles(ports):
    result = []
    for i in ports:
        if i[0] == i[1]:
            result.append([i[0]])
        else:
            result.append(i)
    return result


def validate_input(ports):
    """
    Validates that ports are in correct format
    :param ports: list of lists
    :type ports: list[list]
    :return: bool
    :rtype:
    """
    for i in ports:
        if len(i) == 2 or len(i) == 0:
            return True
        else:
            return False


def apply_port_exclusions(include_ports: list, exclude_ports: list):
    """
    Removes excluded ports from included ports.
    :param include_ports: list of list pairs indicating included ports
    :type include_ports: list[list]
    :param exclude_ports: list of list pairs indicating ports to be excluded
    :type exclude_ports: list[list]
    :return: minimized list of included port ranges
    """
    ports = []
    # sort ports
    include_ports.sort()
    include_ports = remove_doubles(include_ports)
    # get rid of overlapping ports and sort
    for i in range(1, len(exclude_ports)):
        exclude_ports = combine_overlap(exclude_ports[i-1], exclude_ports[i])
    # iterate through include ports and only modify the includes with excludes that conflict
    for i in include_ports:
        for j in exclude_ports:
            if j[0] in range(i[0], i[1]+1):
                ports.append([i[0], j[0]-1])
            if j[1] in range(i[0], i[1]+1):
                ports.append([j[1]+1, i[1]])
            else:
                ports.append([i[0], i[1]])
    # make sure they are still sorted
    ports.sort()
    return ports


def create_parser():
    """
    Create argument parser for command line use
    :return: Argument Parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('include_ports', default=[], type=list, help='ports to include')
    parser.add_argument('exclude_ports', default=[], type=list, help='ports to exclude')
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
            apply_port_exclusions(ns.include_ports, ns.exclude_ports)
    except ValueError:
        print("Invalid input")



if __name__ == '__main__':
    main(sys.argv[1:])