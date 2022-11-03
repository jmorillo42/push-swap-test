#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    push-swap-test.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmorillo <jmorillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/08/16 15:14:35 by jmorillo          #+#    #+#              #
#    Updated: 2022/11/02 22:36:58 by jmorillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import itertools
import math
import os
import random
import subprocess
import sys
import time

RED = '\033[31m'
LRED = '\033[1;31m'
GREEN = '\033[32m'
LGREEN = '\033[1;32m'
BLUE = '\033[34m'
LBLUE = '\033[1;34m'
YELLOW = '\033[1;33m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
GRAY = '\033[1;30m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

#print(f'{YELLOW}Tests {LRED}closed{YELLOW} due to renovations{RESET}')
#exit(0)

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
    print(f'{RED}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RESET}')
    print(f'{RED}┃  {YELLOW}Tests for push-swap project{RESET}  {RED}┃{RESET}')
    print(f'{RED}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}')
    print()
    print(f'{WHITE}INPUT/OUTPUT{RESET}')
    print(f'{GRAY}[OK] push_swap(INPUT) = MOVEMENTS ; STDERR (RETURN_CODE){RESET}')
    print_input_output_tests()
    print()
    print(f'{WHITE}COMBINATIONS OF N NUMBERS{RESET}')
    print(' Show all')
    print(f'  {GRAY}[OK] push_swap(INPUT) = MOVEMENTS ; STDERR (RETURN_CODE){RESET}')
    print_all_comb_numbers(3)
    #print_all_comb_numbers(4)
    #print_all_comb_numbers(5)
    print()
    print(' Only stats')
    print(f'  {GRAY}[OK] N=# --> AVERAGE [MIN - MAX]  POINTS   AVG_TIME{RESET}')
    print_comb_numbers(2)
    print_comb_numbers(3)
    print_comb_numbers(4)
    print_comb_numbers(5)
    print()
    print(f'{WHITE}SEQUENCES OF N NUMBERS{RESET}')
    print(f' {GRAY}[OK] N=### --> AVERAGE [  MIN -   MAX]  POINTS   AVG_TIME{RESET}')
    print_sequence_numbers(50)
    print_sequence_numbers(100)
    print_sequence_numbers(250)
    print_sequence_numbers(500)
    print()
    print(f'{WHITE}T ITERATIONS OF N RANDOM NUMBERS{RESET}')
    print(f' {GRAY}[OK] N=### (T=###) --> AVERAGE [  MIN -   MAX]  POINTS   AVG_TIME{RESET}')
    print_random_numbers(6, 80)
    print_random_numbers(10, 70)
    print_random_numbers(15, 60)
    print_random_numbers(25, 50)
    print_random_numbers(50, 40)
    print_random_numbers(80, 30)
    print_random_numbers(100, 100)
    print_random_numbers(125, 20)
    print_random_numbers(250, 20)
    print_random_numbers(500, 50)
    #print_random_numbers(1000, 10)
    #print_random_numbers(5000, 2)
    print()

def print_input_output_tests() -> None:
    for numbers in TESTS:
        result, actions, ps_err, ps_code = sort_and_check(numbers)
        print_push_swap_results(numbers, result, actions, ps_err, ps_code)

def print_all_comb_numbers(length: int) -> None:
    combinations = calc_comb_numbers(length)
    for numbers in combinations:
        result, actions, ps_err, ps_code = sort_and_check(numbers)
        print_push_swap_results(numbers, result, actions, ps_err, ps_code, '  ')

def print_comb_numbers(length: int) -> None:
    ok, avgm, minm, maxm, exec_time = sort_and_stats(calc_comb_numbers(length))
    points = evaluation_points(length, [avgm, minm, maxm])
    print(f'  {ok_ko_string(ok)} N={LBLUE}{length}{RESET} --> {CYAN}{avgm:7.2f}{RESET} [{LGREEN}{minm:3d}{RESET} - {LRED}{maxm:3d}{RESET}]  {points}  {BLUE}{exec_time:6.2f}ms{RESET}')

def print_sequence_numbers(length: int) -> None:
    ok, avgm, minm, maxm, exec_time = sort_and_stats(calc_sequence_numbers(length))
    points = evaluation_points(length, [avgm, minm, maxm])
    print(f' {ok_ko_string(ok)} N={LBLUE}{length:3d}{RESET} --> {CYAN}{avgm:7.1f}{RESET} [{LGREEN}{minm:5d}{RESET} - {LRED}{maxm:5d}{RESET}]  {points}  {BLUE}{exec_time:6.2f}ms{RESET}')

def print_random_numbers(length: int, iterations: int) -> None:
    ok, avgm, minm, maxm, exec_time = sort_and_stats(calc_random_numbers(length, iterations))
    points = evaluation_points(length, [avgm, minm, maxm])
    print(f' {ok_ko_string(ok)} N={LBLUE}{length:3d}{RESET} (T={LBLUE}{iterations:3d}{RESET}) --> {CYAN}{avgm:7.1f}{RESET} [{LGREEN}{minm:5d}{RESET} - {LRED}{maxm:5d}{RESET}]  {points}  {BLUE}{exec_time:6.2f}ms{RESET}')

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
    return action_count, ps_output, ps_error, ps_rcode

def check_actions(numbers: list, actions: str) -> tuple:
    numbers = [str(n) for n in numbers]
    chk_command = [CHECKER] + numbers
    chk_process = subprocess.run(chk_command, capture_output=True, text=True, input=actions)
    chk_output = chk_process.stdout.strip()
    chk_error = chk_process.stderr.strip()
    chk_rcode = chk_process.returncode
    return chk_output, chk_error, chk_rcode

def compare_outputs(ps_out, ps_err, chk_out, chk_err) -> bool:
    return (chk_out == 'OK' and not ps_err) or (chk_err == ps_err and chk_err in ('', 'Error'))

def sort_and_check(numbers: list) -> tuple:
    count, ps_out, ps_err, ps_code = sort_numbers(numbers)
    chk_out, chk_err, chk_code = check_actions(numbers, ps_out)
    result = compare_outputs(ps_out, ps_err, chk_out, chk_err)
    return result, count, ps_err, ps_code

def sort_and_stats(numbers_list: list) -> tuple:
    total_moves = 0
    min_moves = -1
    max_moves = -1
    start = time.time()
    for numbers in numbers_list:
        result, count, ps_err, ps_code = sort_and_check(numbers)
        if not result:
            break
        total_moves += count
        if count > max_moves:
            max_moves = count
        if count < min_moves or min_moves < 0:
            min_moves = count
    exec_time = (time.time() - start) / len(numbers_list) * 1000
    avg_moves = total_moves / len(numbers_list)
    return result, avg_moves, min_moves, max_moves, exec_time

def print_push_swap_results(numbers: list, result:bool, count: int, ps_err: str, ps_code: int, padding='') -> None:
    ok = ok_ko_string(result)
    numbers = [f'{LBLUE}{n}{RESET}' if isinstance(n, int) else f'{LBLUE}“{n}”{RESET}' for n in numbers]
    count = f'{CYAN}{count}{RESET}'
    ps_err = f'{CYAN}{ps_err if ps_err else "—"}{RESET}'
    ps_code = f'{CYAN}{ps_code}{RESET}'
    sep = f'{GRAY};{RESET}'
    print(f'{padding}{ok} push_swap({", ".join(numbers)}) = {count} {sep} {ps_err} ({ps_code})')

def ok_ko_string(result: bool) -> str:
    if result:
        return f'[{GREEN}OK{RESET}]'
    else:
        return f'[{RED}KO{RESET}]'

def calc_comb_numbers(length: int) -> list:
    numbers = list(range(1, length + 1))
    result = [list(n) for n in itertools.permutations(numbers)]
    return result

def calc_sequence_numbers(length: int) -> list:
    numbers = list(range(1, length + 1))
    result = list()
    result.append(numbers.copy())
    rev = numbers.copy()
    rev.reverse()
    result.append(rev)
    asc1 = list(range(1, length + 1, 2))
    asc2 = list(range(2, length + 1, 2))
    des1 = asc1.copy()
    des1.reverse()
    des2 = asc2.copy()
    des2.reverse()
    result.append(asc1 + asc2)
    result.append(asc1 + des2)
    result.append(des1 + asc2)
    result.append(des1 + des2)
    return result

def calc_random_numbers(length: int, count: int) -> list:
    numbers = list(range(1, length + 1))
    result = list()
    while (count):
        random.seed()
        random.shuffle(numbers)
        result.append(numbers.copy())
        count -= 1
    return result

def evaluation_points(length, stats):
    points = {
        3: points_3(stats),
        5: points_5(stats),
        100: points_100(stats),
        500: points_500(stats),
    }
    return points.get(length, f'{"":7}')

def points_3(stats):
    result = []
    for value in stats:
        if value <= 3:
            result.append(1)
        else:
            result.append(0)
    return points_message(result)

def points_5(stats):
    result = []
    for value in stats:
        if value <= 12:
            result.append(1)
        else:
            result.append(0)
    return points_message(result)

def points_100(stats):
    result = []
    for value in stats:
        if value < 700:
            result.append(5)
        elif value < 900:
            result.append(4)
        elif value < 1100:
            result.append(3)
        elif value < 1300:
            result.append(2)
        elif value < 1500:
            result.append(1)
        else:
            result.append(0)
    return points_message(result)

def points_500(stats):
    result = []
    for value in stats:
        if value < 5500:
            result.append(5)
        elif value < 7000:
            result.append(4)
        elif value < 8500:
            result.append(3)
        elif value < 10000:
            result.append(2)
        elif value < 11500:
            result.append(1)
        else:
            result.append(0)
    return points_message(result)

def points_message(points):
    return f'{CYAN}{points[0]}{RESET} [{LGREEN}{points[1]}{RESET}-{LRED}{points[2]}{RESET}]'

# def complexity_estimation_message(length: int) -> str:
#     complex = math.ceil(math.log(length, 2) * length)
#     return f'{GRAY}n·log n={CYAN}{complex}{RESET}'

if __name__ == "__main__":
    main()
