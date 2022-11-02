#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    push-swap-test.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmorillo <jmorillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/08/16 15:14:35 by jmorillo          #+#    #+#              #
#    Updated: 2022/11/02 14:31:14 by jmorillo         ###   ########.fr        #
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

print(f'{YELLOW}Tests {RED}closed{YELLOW} for renovations{RESET}')
exit(0)

COMMAND_NOT_FOUND = 'Error: Command “{}” not found'
OPSYS_INVALID = 'Error: There is no checker for the operating system “{}”'
INVALID_OUTPUT = 'The action “{}” is not valid'
CRASH = 'push_swap terminated unexpectedly: “{}”'

PUSH_SWAP = '../push-swap/push_swap'
if not os.path.exists(PUSH_SWAP):
    print(COMMAND_NOT_FOUND.format(PUSH_SWAP))
    exit(1)

if os.uname().sysname == 'Darwin':
    CHECKER = './checker_Mac'
elif os.uname().sysname == 'Linux':
    CHECKER = './checker_linux'
else:
    print(OPSYS_INVALID.format(os.uname().sysname))
    exit(1)

if not os.path.exists(CHECKER):
    print(COMMAND_NOT_FOUND.format(CHECKER))
    exit(1)

ACTIONS = ('pa', 'pb', 'ra', 'rb', 'rr', 'rra', 'rrb', 'rrr', 'sa', 'sb', 'ss')

TESTS=[
[],
[''],
[' '],
['+'],
['-'],
[0,],
['-0',],
['+0',],
[' 0',],
[42,],
[-42],
['+42'],
['-+42'],
['--42'],
['+-42'],
['++42'],
['-42-'],
['-42A'],
['00000000000000000000042'],
[' 00000000000000000000042'],
['+00000000000000000000042'],
['-00000000000000000000042'],
[2147483647],
[2147483648],
[-2147483648],
[-2147483649],
[6442450943],
[12345678901234567890],
['+12345678901234567890'],
['-12345678901234567890'],
[' 12345678901234567890'],
['A'],
['FOOBAR'],
['00000000000000000000042', '000000000000000000000'],
['+00000000000000000000042', '+000000000000000000000'],
['-00000000000000000000042', '-000000000000000000000'],
[1, '', 2],
[' 3 2 6 5 4 1 '],
[3, 2, '6 5 4', 1],
[3, 2, '6 5 A', 1],
[-19, -17, -13, -11, -7, -5, -3, -2, -0, 2, 3, 5, 7, 11, 13, 17, 19]
]

def main():
    print('Tests for push-swap project (by jmorillo)')
    print()
    print_input_output_tests()
    print()
    print('COMBINATIONS OF N NUMBERS')
    print(' Show all')
    print(f' {GRAY}[OK] push_swap(INPUT) = [MOVEMENTS ; ERROR ; RETURN CODE]{RESET}')
    print_all_comb_numbers(3)
    #print_all_comb_numbers(4)
    #print_all_comb_numbers(5)
    print(' Only results')
    print_comb_numbers(2)
    print_comb_numbers(3)
    print_comb_numbers(4)
    print_comb_numbers(5)
    #print_comb_numbers(6)
    print()
    print('SEQUENCES OF N NUMBERS')
    print_sequence_numbers(100)
    print_sequence_numbers(500)
    print()
    print('T ITERATIONS OF N RANDOM NUMBERS')
    print_random_numbers(6, 80)
    print_random_numbers(8, 80)
    print_random_numbers(16, 80)
    print_random_numbers(32, 60)
    print_random_numbers(64, 40)
    print_random_numbers(256, 20)
    #print_random_numbers(1024, 10)
    #print_random_numbers(5000, 2)
    print()
    print_random_numbers(100, 100)
    print_random_numbers(500, 50)
    print()

def print_input_output_tests():
    print('INPUT/OUTPUT')
    print(f'{GRAY}[OK] push_swap(INPUT) = [MOVEMENTS ; ERROR ; RETURN CODE]{RESET}')
    for numbers in TESTS:
        result, actions, ps_err, ps_code = sort_and_check(numbers)
        ok = ok_ko_string(result)
        numbers = [f'{BLUE}{n}{RESET}' if isinstance(n, int) else f'{BLUE}“{n}”{RESET}' for n in numbers]
        actions = f'{MAGENTA}{actions}{RESET}'
        ps_err = f'{MAGENTA}{ps_err}{RESET}'
        ps_code = f'{MAGENTA}{ps_code}{RESET}'
        sep = f'{GRAY};{RESET}'
        print(f'{ok} push_swap({", ".join(numbers)}) = [{actions} {sep} {ps_err} {sep} {ps_code}]')

def print_all_comb_numbers(length):
    combinations = calc_comb_numbers(length)
    print(f'  N={length}')
    for numbers in combinations:
        result, actions, ps_err, ps_code = sort_and_check(numbers)
        ok = ok_ko_string(result)
        numbers = [f'{BLUE}{n}{RESET}' if isinstance(n, int) else f'{BLUE}“{n}”{RESET}' for n in numbers]
        actions = f'{MAGENTA}{actions}{RESET}'
        ps_err = f'{MAGENTA}{ps_err}{RESET}'
        ps_code = f'{MAGENTA}{ps_code}{RESET}'
        sep = f'{GRAY};{RESET}'
        print(f'  {ok} push_swap({", ".join(numbers)}) = [{actions} {sep} {ps_err} {sep} {ps_code}]')

def print_comb_numbers(length, rating=True):
    meanm, minm, maxm = sort_test_numbers(calc_comb_numbers(length))
    rating = calc_rating(length, [meanm, minm, maxm]) if rating else ''
    print(f'  {BLUE}N={length}{RESET} --> {MAGENTA}{meanm:.2f}{RESET} [{GREEN}{minm}{RESET}-{RED}{maxm}{RESET}]{rating}')

def print_sequence_numbers(length, rating=True):
    meanm, minm, maxm = sort_test_numbers(calc_sequence_numbers(length))
    rating = calc_rating(length, [meanm, minm, maxm]) if rating else ''
    print(f' {BLUE}N={length}{RESET} --> {MAGENTA}{meanm:.1f}{RESET} [{GREEN}{minm}{RESET}-{RED}{maxm}{RESET}]{rating}')

def print_random_numbers(length, count, rating=True):
    meanm, minm, maxm = sort_test_numbers(calc_random_numbers(length, count))
    rating = calc_rating(length, [meanm, minm, maxm]) if rating else ''
    print(f' {BLUE}N={length} (T={count}){RESET} --> {MAGENTA}{meanm:.1f}{RESET} [{GREEN}{minm}{RESET}-{RED}{maxm}{RESET}]{rating}')

def sort_numbers(numbers: list) -> tuple:
    numbers = [str(n) for n in numbers]

    ps_command = [PUSH_SWAP] + numbers
    ps_process = subprocess.run(ps_command, capture_output=True, text=True)
    ps_output = ps_process.stdout
    ps_error = ps_process.stderr.strip()
    ps_rcode = ps_process.returncode
    if ps_error and ps_error != 'Error':
        ps_error = CRASH.format(ps_error)
    action_lines = ps_output.splitlines()
    action_count = 0
    for line in action_lines:
        if line in ACTIONS:
            action_count += 1
        else:
            ps_error = INVALID_OUTPUT.format(line)

    # print('PUSH-SWAP')
    # print(f' actions->{"·".join(action_lines)}')
    # print(f' count--->{action_count}')
    # print(f' error--->{ps_error}')
    # print(f' rcode--->{ps_rcode}')
    return action_count, ps_output, ps_error, ps_rcode

def check_actions(numbers: list, actions: str) -> tuple:
    numbers = [str(n) for n in numbers]

    chk_command = [CHECKER] + numbers
    chk_process = subprocess.run(chk_command, capture_output=True, text=True, input=actions)
    chk_output = chk_process.stdout.strip()
    chk_error = chk_process.stderr.strip()
    chk_rcode = chk_process.returncode

    # print('CHECKER')
    # chk_args = ','.join(chk_process.args[1:])
    # print(f' args---->{chk_args}')
    # print(f' output-->{chk_output}')
    # print(f' error--->{chk_error}')
    # print(f' rcode--->{chk_rcode}')
    return chk_output, chk_error, chk_rcode

def compare_outputs(ps_out, ps_err, chk_out, chk_err) -> bool:
    # return chk_out == 'OK' or (chk_err == 'Error' and ps_err) or (chk_out == '' and not ps_err and not ps_out.strip())
    return (chk_out == 'OK' and not ps_err) or (chk_err == ps_err and chk_err in ('', 'Error'))

def sort_and_check(numbers: list) -> tuple:
    count, ps_out, ps_err, ps_code = sort_numbers(numbers)
    chk_out, chk_err, chk_code = check_actions(numbers, ps_out)
    result = compare_outputs(ps_out, ps_err, chk_out, chk_err)
    return result, count, ps_err, ps_code

def ok_ko_string(result: bool) -> str:
    if result:
        return f'[{GREEN}OK{RESET}]'
    else:
        return f'[{RED}KO{RESET}]'

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
    numbers = list(range(1, length + 1))
    result = [list(n) for n in itertools.permutations(numbers)]
    return result

def calc_sequence_numbers(length):
    numbers = [str(n) for n in range(1, length + 1)]
    result = list()
    result.append(numbers.copy())
    rev = numbers.copy()
    rev.reverse()
    result.append(rev)
    asc = list(range(1, length + 1, 2))
    des = list(range(2, length + 1, 2))
    des.reverse()
    result.append(asc + des)
    result.append(des + asc)
    return result

def calc_random_numbers(length, count):
    numbers = list(range(1, length + 1))
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
        actions, ps_err, ps_code, chk_out, chk_err, chk_code = sort_numbers(numbers, check)
        if ps_err or chk_out != 'OK':
            total_moves = 0
            min_moves = -1
            max_moves = -1
            break
        total_moves += actions
        if actions > max_moves:
            max_moves = actions
        if actions < min_moves:
            min_moves = actions
    mean_moves = total_moves / len(tests)
    return mean_moves, min_moves, max_moves

def calc_rating(length, moves):
    if moves[1] < 0:
        result = f'  [{RED}KO{RESET}]'
    else:
        result = f'  {rating_message(length, moves)}'
    return result

if __name__ == "__main__":
    main()
