#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ᲙᲚᲐᲕᲘᲐᲢᲣᲠᲘᲡ ᲢᲠᲔᲜᲐᲟᲝᲠᲘ

"""
import sys
import termios
import tty

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def load_sequences(filename):
    with open(filename, 'r') as file:
        return [line.rstrip('\n') for line in file]

def save_level(level):
    with open('score.txt', 'a') as file:  # Используем режим 'a' для добавления
        file.write(f"შეფასება: {level}\n")

def run_sequence_test(sequence):
    extended_sequence = sequence * 20
    print(f"უნდა გამოწერო შედეგი კომბინაცია: {sequence}")
    print("გამოსასვლელად უდა დაჭირო <Esc>-ს.")
    user_input = ''
    for expected_char in extended_sequence:
        char = getch()
        if ord(char) == 27:  # ASCII код для <Esc>
            print("\nპროგრამიდან გასვლა.")
            sys.exit(0)
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != expected_char:
            print("\nშეცდომა. მისია ჩაიშალა.")
            return False
    return True

if __name__ == '__main__':
    sequences = load_sequences("sequence.txt")

    for i,sequence in enumerate(sequences):
        while not run_sequence_test(sequence):
            print("\n დაიწყე თავიდან.")

        print("\nგილოცავ, მისია გავლილია!")
        save_level(i + 1)
        if i == len(sequences) - 1:
            print("\nსავარჯიშოები ამით ამოწურულია, შენი შეფასება ათიანი!")
        elif input("'გადავიდეთ შემდეგზე? (Y/n) ") != 'y':
            sys.exit(0)
