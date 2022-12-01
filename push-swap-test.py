#!/usr/bin/env python3

import itertools
import math
import os
import random
import signal
import subprocess
import sys
import time

from config import PUSH_SWAP, CHECKER, INPUT_TESTS, COMB_ALL_TESTS, COMB_STAT_TESTS, SEQ_TESTS, RANDOM_TESTS, CHECKER_TESTS

RED = '\033[0;31m'
LRED = '\033[1;31m'
GREEN = '\033[0;32m'
LGREEN = '\033[1;32m'
BLUE = '\033[0;34m'
LBLUE = '\033[1;34m'
CYAN = '\033[1;36m'
MAGENTA = '\033[1;35m'
YELLOW = '\033[1;33m'
GRAY = '\033[1;30m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

UPDATED = '2022-12-01 13:43'

COMMAND_NOT_FOUND = f'{RED}Error: Command “{YELLOW}{{}}{RED}” not found{RESET}'
OPSYS_INVALID = 'Error: There is no checker for the operating system “{}”'
INVALID_OUTPUT = f'{RED}INVALID OUTPUT "{{}}"{RESET}'
CRASH = f'{RED}CRASH{RESET}'
TIMEOUT = f'{RED}TIMEOUT{RESET}'
MISMATCH = f'{RED}MISMATCH:"{YELLOW}{{}}{RED}"{RESET}'
SEGFAULT = f'{RED}SEGFAULT{RESET}'
BUSERROR = f'{RED}BUS{RESET}'

if os.uname().sysname == 'Darwin':
    CHECKER_42 = './checker_Mac'
elif os.uname().sysname == 'Linux':
    CHECKER_42 = './checker_linux'
else:
    print(OPSYS_INVALID.format(os.uname().sysname))
    exit(1)

if not os.path.exists(CHECKER_42):
    print(COMMAND_NOT_FOUND.format(CHECKER_42))
    exit(1)

BONUS = os.path.exists(CHECKER)

ACTIONS = ('pa', 'pb', 'ra', 'rb', 'rr', 'rra', 'rrb', 'rrr', 'sa', 'sb', 'ss')

def main():
    BOX = WHITE
    LOGO = GRAY
    print(f'{BOX}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RESET}')
    print(f'{BOX}┃                                                                              {BOX}┃{RESET}')
    print(f'{BOX}┃                                                         {LOGO}:::      ::::::::    {BOX}┃{RESET}')
    print(f'{BOX}┃    {LGREEN}PUSH-SWAP TESTS                                    {LOGO}:+:      :+:    :+:    {BOX}┃{RESET}')
    print(f'{BOX}┃                                                     {LOGO}+:+ +:+         +:+      {BOX}┃{RESET}')
    print(f'{BOX}┃    {LGREEN}By: jmorillo <jmorillo@student.42.fr>          {LOGO}+#+  +:+       +#+         {BOX}┃{RESET}')
    print(f'{BOX}┃                                                 {LOGO}+#+#+#+#+#+   +#+            {BOX}┃{RESET}')
    print(f'{BOX}┃    {GREEN}Created: 2022-08-16 15:14                         {LOGO}#+#    #+#              {BOX}┃{RESET}')
    print(f'{BOX}┃    {GREEN}Updated: {UPDATED:16}                        {LOGO}###   ########.fr        {BOX}┃{RESET}')
    print(f'{BOX}┃                                                                              ┃{RESET}')
    print(f'{BOX}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}')
    print()

    if not os.path.exists(PUSH_SWAP):
        print(COMMAND_NOT_FOUND.format(PUSH_SWAP))
        exit(1)

    print()
    print(f'{WHITE}INPUT/OUTPUT{RESET}')
    print(f' {GRAY}[OK] push_swap(INPUT) = MOVEMENTS ; STDERR (RETURN_CODE){RESET}')
    print_input_output_tests()
    print()
    print(f'{WHITE}COMBINATIONS OF N NUMBERS{RESET}')
    print(f' {GRAY}[OK] push_swap(INPUT) = MOVEMENTS ; STDERR (RETURN_CODE){RESET}')
    for n in COMB_ALL_TESTS:
        print_all_comb_numbers(n)
    print()
    print(' Only stats')
    print(f'  {GRAY}[OK] N=# --> AVERAGE [MIN - MAX]  POINTS   AVG_TIME{RESET}')
    for n in COMB_STAT_TESTS:
        print_comb_numbers(n)
    print()
    print(f'{WHITE}SEQUENCES OF N NUMBERS{RESET}')
    print(f' {GRAY}[OK] N=### --> AVERAGE [  MIN -   MAX]  POINTS   AVG_TIME{RESET}')
    for n in SEQ_TESTS:
        print_sequence_numbers(n)
    print()
    print(f'{WHITE}T ITERATIONS OF N RANDOM NUMBERS{RESET}')
    print(f' {GRAY}[OK] N=### (T=###) --> AVERAGE [  MIN -   MAX]  POINTS   AVG_TIME{RESET}')
    for n, t in RANDOM_TESTS:
        print_random_numbers(n, t)
    print()
    print(f'{WHITE}BONUS{RESET}')
    if BONUS:
        print(f' {GRAY}[OK] checker(INPUT ; STDIN) = OUTPUT ; STDERR (RETURN_CODE)  CHECKER42 (CODE){RESET}')
        print_checker_tests()
    else:
        print(COMMAND_NOT_FOUND.format(CHECKER))
    print()

def print_input_output_tests() -> None:
    for numbers in INPUT_TESTS:
        result, actions, ps_err, ps_code = sort_and_check(numbers)
        print_push_swap_results(numbers, result, actions, ps_err, ps_code)

def print_all_comb_numbers(length: int) -> None:
    combinations = calc_comb_numbers(length)
    for numbers in combinations:
        result, actions, ps_err, ps_code = sort_and_check(numbers)
        print_push_swap_results(numbers, result, actions, ps_err, ps_code)

def print_comb_numbers(length: int) -> None:
    ok, avgm, minm, maxm, exec_time = sort_and_stats(calc_comb_numbers(length))
    points = evaluation_points(length if ok else -1, [avgm, minm, maxm])
    print(f'  {ok_ko_string(ok)} N={LBLUE}{length}{RESET} --> {CYAN}{avgm:7.2f}{RESET} [{LGREEN}{minm:3d}{RESET} - {LRED}{maxm:3d}{RESET}]  {points}  {exec_time:6.2f}ms')

def print_sequence_numbers(length: int) -> None:
    ok, avgm, minm, maxm, exec_time = sort_and_stats(calc_sequence_numbers(length))
    points = evaluation_points(length if ok else -1, [avgm, minm, maxm])
    print(f' {ok_ko_string(ok)} N={LBLUE}{length:3d}{RESET} --> {CYAN}{avgm:7.1f}{RESET} [{LGREEN}{minm:5d}{RESET} - {LRED}{maxm:5d}{RESET}]  {points}  {exec_time:6.2f}ms')

def print_random_numbers(length: int, iterations: int) -> None:
    ok, avgm, minm, maxm, exec_time = sort_and_stats(calc_random_numbers(length, iterations))
    points = evaluation_points(length if ok else -1, [avgm, minm, maxm])
    print(f' {ok_ko_string(ok)} N={LBLUE}{length:3d}{RESET} (T={LBLUE}{iterations:3d}{RESET}) --> {CYAN}{avgm:7.1f}{RESET} [{LGREEN}{minm:5d}{RESET} - {LRED}{maxm:5d}{RESET}]  {points}  {exec_time:6.2f}ms')

def print_checker_tests() -> None:
    for numbers, actions in CHECKER_TESTS:
        chk_out, chk_err, chk_code = check_numbers_and_actions(numbers, actions)
        chk42_out, chk42_err, chk42_code = check_actions(numbers, actions)
        ok = compare_checkers(chk_out, chk_err, chk42_out, chk42_err)
        ok = ok_ko_string(ok)
        input_numbers = []
        for n in numbers:
            if isinstance(n, str):
                n = f'“{replace_non_printable(n)}”'
            input_numbers.append(f'{LBLUE}{n}{RESET}')
        actions = f'“{LBLUE}{replace_non_printable(actions)}{RESET}”'
        chk_out = f'{CYAN}{chk_out.strip() if chk_out.strip() else "—"}{RESET}'
        chk_err = f'{CYAN}{chk_err.strip() if chk_err else "—"}{RESET}'
        chk_code = f'{CYAN}{chk_code}{RESET}'
        chk42_result = f'{GRAY}{chk42_out.strip() if chk42_out.strip() else chk42_err.strip()} ({chk42_code}){RESET}'
        sep = f'{GRAY};{RESET}'
        print(f' {ok} checker([{", ".join(input_numbers)}] ; {actions}) = {chk_out} {sep} {chk_err} ({chk_code})  {chk42_result}')

def sort_numbers(numbers: tuple) -> tuple:
    numbers = [str(n) for n in numbers]
    ps_command = [PUSH_SWAP] + numbers
    action_count = 0
    ps_output = ''
    ps_rcode = 1
    try:
        ps_process = subprocess.run(ps_command, capture_output=True, text=True, timeout=1)
        ps_output = ps_process.stdout
        ps_error = ps_process.stderr
        ps_rcode = ps_process.returncode
        if -ps_rcode == signal.SIGSEGV:
            ps_error = SEGFAULT
        elif -ps_rcode == signal.SIGBUS:
            ps_error = BUSERROR
        elif (ps_rcode != 0 or ps_error) and (ps_rcode == 0 or ps_error != 'Error\n'):
            ps_error = MISMATCH.format(ps_error)
        else:
            action_lines = ps_output.splitlines()
            for line in action_lines:
                if line in ACTIONS:
                    action_count += 1
                else:
                    ps_error = INVALID_OUTPUT.format(line)
    except subprocess.TimeoutExpired:
        ps_error = TIMEOUT
    except subprocess.CalledProcessError as ex:
        ps_error = CRASH
        ps_rcode = ex.returncode
    return action_count, ps_output, ps_error, ps_rcode

def check_actions(numbers: tuple, actions: str) -> tuple:
    numbers = [str(n) for n in numbers]
    chk_command = [CHECKER_42] + numbers
    chk_process = subprocess.run(chk_command, capture_output=True, text=True, input=actions)
    chk_output = chk_process.stdout
    chk_error = chk_process.stderr
    chk_rcode = chk_process.returncode
    return chk_output, chk_error, chk_rcode

def compare_outputs(ps_out, ps_err, chk_out, chk_err) -> bool:
    return chk_out != 'KO\n' and ((chk_out == 'OK\n' and not ps_err) or (chk_err == ps_err and chk_err in ('', 'Error\n')))

def check_numbers_and_actions(numbers: tuple, actions: str) -> tuple:
    numbers = [str(n) for n in numbers]
    chk_command = [CHECKER] + numbers
    try:
        chk_process = subprocess.run(chk_command, capture_output=True, text=True, input=actions)
        chk_output = chk_process.stdout
        chk_error = chk_process.stderr
        chk_rcode = chk_process.returncode
        if -chk_rcode == signal.SIGSEGV:
            chk_error = SEGFAULT
        elif -chk_rcode == signal.SIGBUS:
            chk_error = BUSERROR
    except subprocess.TimeoutExpired:
        chk_error = TIMEOUT
    except subprocess.CalledProcessError as ex:
        chk_error = CRASH
        chk_rcode = ex.returncode
    return chk_output, chk_error, chk_rcode

def compare_checkers(chk_out, chk_err, chk42_out, chk42_err) -> bool:
    return (chk_out == chk42_out) and (chk_err == chk42_err)

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

def print_push_swap_results(numbers: list, result:bool, count: int, ps_err: str, ps_code: int) -> None:
    ok = ok_ko_string(result)
    input_numbers = []
    for n in numbers:
        if isinstance(n, str):
            n = f'“{replace_non_printable(n)}”'
        input_numbers.append(f'{LBLUE}{n}{RESET}')
    count = f'{CYAN}{count}{RESET}'
    ps_err = f'{CYAN}{ps_err.strip() if ps_err else "—"}{RESET}'
    ps_code = f'{CYAN}{ps_code}{RESET}'
    sep = f'{GRAY};{RESET}'
    print(f' {ok} push_swap({", ".join(input_numbers)}) = {count} {sep} {ps_err} ({ps_code})')

def replace_non_printable(text: str) -> str:
    return "".join([c if ord(c) >= 32 else f"{BLUE}0x{ord(c):02X}{LBLUE}" for c in text])

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
        -1: points_message((0, 0, 0)),
        3: points_3(stats),
        5: points_5(stats),
        100: points_100(stats),
        500: points_500(stats),
    }
    return points.get(length, f'{"":7}')

def points_3(stats):
    result = []
    for value in stats:
        if value <= 3 and value >= 0:
            result.append(1)
        else:
            result.append(0)
    return points_message(result)

def points_5(stats):
    result = []
    for value in stats:
        if value <= 12 and value >= 0:
            result.append(1)
        else:
            result.append(0)
    return points_message(result)

def points_100(stats):
    result = []
    for value in stats:
        if value < 0 or value >= 1500:
            result.append(0)
        elif value < 700:
            result.append(5)
        elif value < 900:
            result.append(4)
        elif value < 1100:
            result.append(3)
        elif value < 1300:
            result.append(2)
        else:
            result.append(1)
    return points_message(result)

def points_500(stats):
    result = []
    for value in stats:
        if value < 0 or value >= 11500:
            result.append(0)
        elif value < 5500:
            result.append(5)
        elif value < 7000:
            result.append(4)
        elif value < 8500:
            result.append(3)
        elif value < 10000:
            result.append(2)
        else:
            result.append(1)
    return points_message(result)

def points_message(points):
    return f'{CYAN}{points[0]}{RESET} [{LGREEN}{points[1]}{RESET}-{LRED}{points[2]}{RESET}]'

# def complexity_estimation_message(length: int) -> str:
#     complex = math.ceil(math.log(length, 2) * length)
#     return f'{GRAY}n·log n={CYAN}{complex}{RESET}'

if __name__ == "__main__":
    main()
