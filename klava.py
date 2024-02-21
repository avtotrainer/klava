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
    repeated_sequence = 80 // len(sequence)  # 10
    extended_sequence = sequence * repeated_sequence  # 20
    green_background =   "\033[42m"# ANSI код для зеленого цвета
    red_text = "\033[91m"  # ANSI код для красного цвета
    bold_text = "\033[1m"  # Жирный
    yellow_text = "\033[93m"  # Желтый для фона
    reset_text = "\033[0m"  # Сброс цвета к стандартному

    print(f"დავალება - დაბეჯდე:{red_text}{bold_text} {green_background}{sequence.replace(' ', '␣')}{reset_text} - ␣ სიმბოლო არის პრობელი (Space)")
    print(f"გამოსასვლელად უდა დაჭირო {red_text} <Esc> {reset_text}-ს.")
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
        if i >= max_level:
            while not run_sequence_test(sequence):
                print("\n დაიწყე თავიდან.")

            print("\nგილოცავ, მისია გავლილია!")
            save_level(i + 1)
            if i == len(sequences) - 1:
                print("\nსავარჯიშოები ამით ამოწურულია, შენი შეფასება ათიანი!")
            elif input("'გადავიდეთ შემდეგზე? (Y/n) ") != 'y':
                sys.exit(0)
