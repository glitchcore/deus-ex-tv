import sys
import select
import string
import random
import shutil
from time import sleep

def slow_print(text, timeout=0.04, pause=0.3):
    for char in text:
        print(char, end='', flush=True)
        sleep(timeout if char not in ['.', ',', '?', ':', '!'] else pause)

def blink_message(message, delay):
    # hide cursor
    print("\033[?25l", end='', flush=True)

    while True:
        print(message, end="", flush=True)
        sleep(delay)
        print("\r" + " " * len(message) + "\r", end="", flush=True)
        sleep(delay)

        # Check for input without blocking
        if select.select([sys.stdin,],[],[],0.0)[0]:
            input_str = input()
            if input_str == "":
                break
    
    # show cursor
    print("\033[?25h", end='', flush=True)

def random_chars(delay, n):
    size = shutil.get_terminal_size()
    printable_chars = string.printable.translate(str.maketrans('', '', string.ascii_letters))

    # move cursor to top-left
    print("\033[1;1H", end='', flush=True)
    
    for i in range(n):
        # move cursor to random point
        row = random.randint(1, size[1] - 1)
        col = random.randint(1, size[0])
        print("\033[{};{}H".format(row, col), end='', flush=True)
        
        # place random character
        char = random.choice(printable_chars)
        print(char, end='', flush=True)
        
        # sleep for delay seconds
        if i % 50 == 0:
            sleep(delay)