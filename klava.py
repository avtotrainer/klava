#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ᲙᲚᲐᲕᲘᲐᲢᲣᲠᲘᲡ ᲢᲠᲔᲜᲐᲟᲝᲠᲘ

"""
import sys
import termios
import tty
ART_LOADED = False
try:
    import art
    ART_LOADED = True
except ImportError:
    pass

GREEN_BACKGROUND =   "\033[42m" # ტექსტი მწვანედ
RED_TEXT = "\033[91m"  # ტექსტი წითლად
BOLD_TEXT = "\033[1m"  # მსხვილი სიმბოლოები
YELLOW_TEXT = "\033[93m"  # ტექსტი ყვითლად
RESET_TEXT = "\033[0m"  # ფერების გარესეტება

def getch():
    """
     სიმბოლოს წაკითხვა კლავიტურიდან
    """
    file_no = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_no)
    try:
        tty.setraw(sys.stdin.fileno())
        read_char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_no, termios.TCSADRAIN, old_settings)
    return read_char

def load_sequences(filename):
    """
     სტრიქონების წაკითხვა ფაილიდან

    """
    with open(filename, 'r') as file:
        return [line.rstrip('\n') for line in file]

def save_level(level):
    """
        ლეველის ჩაწერა
    """
    with open('score.txt', 'a') as file:  # Иa' для добавления
        file.write(f"შეფასება: {level}\n")


def run_sequence_test(sequence):
    """
        ტრენაჟორი

    """
    global ART_LOADED
    if  ART_LOADED:
        print("\033[2J","\033[4;1H", end="")
        # print(art.text2art(sequence))
        print(art.text2art(sequence.replace(' ', '      ')*2))
        print("\033[26;1H", end="")
        print(art.text2art(str(i)))
    else:
        print("\033[2J", end="")
    print("\033[14;10H", end="")
    print(f"ᲓᲐᲕᲐᲚᲔᲑᲐ - დაბეჯდე:{RED_TEXT} {BOLD_TEXT} {GREEN_BACKGROUND}{sequence.replace(' ', '␣')}{RESET_TEXT} - ␣ სიმბოლო არის პრობელი (Space)")
    print("\033[24;10H", end="")
    print(f"გამოსასვლელად უდა დაჭირო {RED_TEXT} <Esc> {RESET_TEXT} ")
    print("\033[18;10H", end="")
    repeated_sequence = 80 // len(sequence)  # 10
    extended_sequence = sequence * repeated_sequence  # 20
    user_input = ''
    for expected_char in extended_sequence:
        char = getch()
        if ord(char) == 27:  # ASCII код для <Esc>
            print("\nᲞᲠᲝᲒᲠᲐᲛᲘᲓᲐᲜ ᲒᲐᲡᲕᲚᲐ.")
            sys.exit(0)
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != expected_char:
            print("\nᲨᲔᲪᲓᲝᲛᲐ: მისია ჩაიშალა.")
            return False
    return True
def find_max_level(filename='score.txt'):
    max_level = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    try:
                        level = int(parts[1])
                        if level > max_level:
                            max_level = level
                    except ValueError:
                        continue
    except FileNotFoundError:
        # Если файл не найден, создаем его и возвращаем начальный уровень 0
        with open(filename, 'w') as file:
            print(f"Файл {filename} создан.")
    return max_level

# Вызываем функцию и печатаем результат

if __name__ == '__main__':
    sequences = load_sequences("sequence.txt")

    max_level = find_max_level()
    for i,sequence in enumerate(sequences):
        if len(sequence) == 0:
            
            print("\nსავარჯიშოები ამით ამოწურულია, შენი შეფასება ათიანი!")
            sys.exit(0)
        if i >= max_level:
            while not run_sequence_test(sequence):
                print("\n დაიწყე თავიდან.")

            print("\nგილოცავ, მისია გავლილია!")
            save_level(i + 1)
            if input("'გადავიდეთ შემდეგზე? (Y/n) ") != 'y':
                sys.exit(0)
