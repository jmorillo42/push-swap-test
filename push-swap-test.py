#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmorillo <jmorillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/08/16 15:14:35 by jmorillo          #+#    #+#              #
#    Updated: 2022/08/19 15:53:16 by jmorillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import itertools
import math
import os
import random
import re
import subprocess
import sys

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[1;34m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
GRAY = '\033[1;30m'
RESET = '\033[0m'

PUSH_SWAP = '../push-swap/push_swap'
if not os.path.exists(PUSH_SWAP):
    print(f'No existe el comando "{PUSH_SWAP}"')
    exit()

if os.uname().sysname == 'Darwin':
    CHECKER = './checker_Mac'
elif os.uname().sysname == 'Linux':
    CHECKER = './checker_linux'
else:
    print(f'No existe "checker" para {os.uname().sysname}')
    exit()

TESTS=[
[],
[''],
[' '],
['+'],
['-'],
[42,],
[-42],
['+42'],
['-+42'],
['--42'],
['+-42'],
['-42-'],
['-42A'],
['000000000000000000000000000042'],
['+000000000000000000000000000042'],
['-000000000000000000000000000042'],
[2147483647],
[2147483648],
[-2147483648],
[-2147483649],
[6442450943],
[12345678901234567890123456789],
['+12345678901234567890123456789'],
['-12345678901234567890123456789'],
['A'],
['FOOBAR'],
['000000000000000000000000000042', '0000000000000000000000000000'],
['+000000000000000000000000000042', '+0000000000000000000000000000'],
['-000000000000000000000000000042', '-0000000000000000000000000000'],
[1, '', 2],
['3 2 6 5 4 1'],
[3, 2, '6 5 4', 1],
[3, 2, '6 5 A', 1],
[-19, -17, -13, -11, -7, -5, -3, -2, 2, 3, 5, 7, 11, 13, 17, 19]
]


def sort_numbers(numbers, check=True):
    ps_command = [PUSH_SWAP] + numbers
    ps_response = b''
    error = False
    try:
        ps_response = subprocess.check_output(ps_command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as ex:
        if (ex.output.decode().strip() == 'Error'):
            error = True
        else:
            print(f'  Error en push_swap: "{ex.output.decode().strip()}" (code={ex.returncode})')
            exit(1)
    steps = ps_response.decode().strip()
    step_count = len(steps.splitlines())
    if check:
        check_command = [CHECKER] + numbers
        try:
            p = subprocess.Popen(check_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout_data = p.communicate(input=ps_response)[0]
        except subprocess.CalledProcessError as ex:
            print(f'  Error en checker: {ex.returncode}')
        check_result = stdout_data.decode().strip()
    else:
        check_result = ""
    return step_count, error, check_result

def points_3(moves):
    result = []
    for move in moves:
        if move <= 3:
            result.append(1)
        else:
            result.append(0)
    return result

def points_5(moves):
    result = []
    for move in moves:
        if move <= 12:
            result.append(1)
        else:
            result.append(0)
    return result

def points_100(moves):
    result = []
    for move in moves:
        if move < 700:
            result.append(5)
        elif move < 900:
            result.append(4)
        elif move < 1100:
            result.append(3)
        elif move < 1300:
            result.append(2)
        elif move < 1500:
            result.append(1)
        else:
            result.append(0)
    return result

def points_500(moves):
    result = []
    for move in moves:
        if move < 5500:
            result.append(5)
        elif move < 7000:
            result.append(4)
        elif move < 8500:
            result.append(3)
        elif move < 10000:
            result.append(2)
        elif move < 11500:
            result.append(1)
        else:
            result.append(0)
    return result

def points_message(points):
    return f'{YELLOW}→ {BLUE}puntos: {MAGENTA}{points[0]}{GRAY} [{GREEN}{points[1]}{GRAY}-{RED}{points[2]}{GRAY}]{RESET}'

def complex_message(length):
    complex = math.ceil(math.log(length, 2) * length)
    return f'{YELLOW}← {BLUE}n·log n{GRAY}={CYAN}{complex}{RESET}'

def rating_message(length, moves):
    if length == 3:
        return points_message(points_3(moves))
    if length == 5:
        return points_message(points_5(moves))
    if length == 100:
        return points_message(points_100(moves))
    if length == 500:
        return points_message(points_500(moves))
    else:
        return complex_message(length)

def calc_comb_numbers(length):
    numbers = [str(n) for n in range(1, length + 1)]
    result = [list(n) for n in itertools.permutations(numbers)]
    return result

def calc_sequence_numbers(length):
    numbers = [str(n) for n in range(1, length + 1)]
    result = list()
    result.append(numbers.copy())
    rev = numbers.copy()
    rev.reverse()
    result.append(rev)
    asc = [str(n) for n in range(1, length + 1, 2)]
    des = [str(n) for n in range(2, length + 1, 2)]
    des.reverse()
    result.append(asc + des)
    result.append(des + asc)
    return result

def calc_random_numbers(length, count):
    numbers = [str(n) for n in range(1, length + 1)]
    result = list()
    while (count):
        random.seed()
        random.shuffle(numbers)
        result.append(numbers.copy())
        count -= 1
    return result

def sort_test_numbers(tests: list, check=True):
    total_moves = 0
    min_moves = sys.maxsize
    max_moves = 0
    for numbers in tests:
        moves, error, check = sort_numbers(numbers, check)
        if error or check != 'OK':
            total_moves = 0
            min_moves = -1
            max_moves = -1
            break
        total_moves += moves
        if moves > max_moves:
            max_moves = moves
        if moves < min_moves:
            min_moves = moves
    mean_moves = total_moves / len(tests)
    return mean_moves, min_moves, max_moves

def print_all_comb_numbers(length):
    randoms = calc_comb_numbers(length)
    for numbers in randoms:
        moves, error, check = sort_numbers(numbers)
        if check == 'OK' or (check == 'Error' and error) or (check == '' and not error and not moves):
            check = f'[{GREEN}OK{RESET}]'
        elif check == 'KO':
            check = f'[{RED}KO{RESET}]'
        moves = f'{MAGENTA}{moves}{RESET}' if not error else f'{CYAN}Error{RESET}'
        numbers = [f'{BLUE}{n}{RESET}' for n in numbers]
        print(f'combination({", ".join(numbers)}) --> {moves} {check}')

def calc_rating(length, moves):
    if moves[1] < 0:
        result = f'  [{RED}KO{RESET}]'
    else:
        result = f'  {rating_message(length, moves)}'
    return result

def print_comb_numbers(length, rating=True):
    meanm, minm, maxm = sort_test_numbers(calc_comb_numbers(length))
    rating = calc_rating(length, [meanm, minm, maxm]) if rating else ''
    print(f'{BLUE}Combinaciones de {length}{RESET} --> {MAGENTA}{meanm:.2f}{RESET} [{GREEN}{minm}{RESET}-{RED}{maxm}{RESET}]{rating}')

def print_sequence_numbers(length, rating=True):
    meanm, minm, maxm = sort_test_numbers(calc_sequence_numbers(length))
    rating = calc_rating(length, [meanm, minm, maxm]) if rating else ''
    print(f'{BLUE}Secuencias de {length}{RESET} --> {MAGENTA}{meanm:.1f}{RESET} [{GREEN}{minm}{RESET}-{RED}{maxm}{RESET}]{rating}')

def print_random_numbers(length, count, rating=True):
    meanm, minm, maxm = sort_test_numbers(calc_random_numbers(length, count))
    rating = calc_rating(length, [meanm, minm, maxm]) if rating else ''
    print(f'{BLUE}{length} aleatorios ({count} rep.){RESET} --> {MAGENTA}{meanm:.1f}{RESET} [{GREEN}{minm}{RESET}-{RED}{maxm}{RESET}]{rating}')

def main():
    print()
    for numbers in TESTS:
        moves, error, check = sort_numbers([str(n) for n in numbers])
        if check == 'OK' or (check == 'Error' and error) or (check == '' and not error and not moves):
            check = f'[{GREEN}OK{RESET}]'
        else:
            check = f'[{RED}KO{RESET}]'
        moves = f'{MAGENTA}{moves}{RESET}' if not error else f'{CYAN}Error{RESET}'
        numbers = [f'{BLUE}{n}{RESET}' if isinstance(n, int) else f'{BLUE}“{n}”{RESET}' for n in numbers]
        print(f'push_swap({", ".join(numbers)}) --> {moves} {check}')
    print()
    print_all_comb_numbers(3)
    #print_all_comb_numbers(4)
    #print_all_comb_numbers(5)
    print()
    print_comb_numbers(2)
    print_comb_numbers(4)
    #print_comb_numbers(6)
    print()
    print_sequence_numbers(100)
    print_sequence_numbers(500)
    print()
    print_random_numbers(6, 80)
    print_random_numbers(8, 80)
    print_random_numbers(16, 80)
    print_random_numbers(32, 60)
    print_random_numbers(64, 40)
    print_random_numbers(256, 20)
    #print_random_numbers(1024, 10)
    #print_random_numbers(5000, 2)
    print()
    print_comb_numbers(3)
    print_comb_numbers(5)
    print_random_numbers(100, 100)
    print_random_numbers(500, 50)
    print()

if __name__ == "__main__":
    main()
