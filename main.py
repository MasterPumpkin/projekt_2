"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Josef Nuhlíček
email: josef.nuhlicek@gmail.com
"""
import random
from typing import List, Tuple

# Separator line for console output
SEPARATOR_LINE = '-' * 47

def enter_guessed_numbers() -> str:
    """
    Prompts the user to enter a number and validates the input.

    Repeatedly asks for input until the user enters a valid 4-digit number.
    The number must contain only digits, must not start with zero, and all
    digits must be unique.

    Returns:
        str: The validated user input as a string.
    """
    is_guessed_number_ok = False
    while not is_guessed_number_ok:
        guessed_numbers = input(">>> ").strip()
        if not guessed_numbers.isdigit():
            print('Input contains a non-numeric character, try again.')
        elif len(guessed_numbers) != 4:
            print('Please enter just 4 digits, try again.')
        elif guessed_numbers[0] == '0':
            print('The number must not start with zero, try again.')
        elif len(set(guessed_numbers)) < 4:
            print('The number contains duplicate digits, please try again.')
        else:
            is_guessed_number_ok = True
    return guessed_numbers


def get_correct_form_of_word(bulls: int, cows: int) -> Tuple[str, str]:
    """
    Returns the correct grammatical forms of the words "bull" and "cow".

    Args:
        bulls (int): The number of "bulls" (correct digit 
                     in the correct position).
        cows (int): The number of "cows" (correct digit 
                     in the wrong position).

    Returns:
        Tuple[str, str]: A tuple with the correct forms 
                         of the words "bull" and "cow".
    """
    bull_word = 'bull' if bulls == 1 else 'bulls'
    cow_word = 'cow' if cows == 1 else 'cows'
    return bull_word, cow_word


def generate_numbers_for_guessing() -> List[int]:
    """
    Generates a random 4-digit secret number to be guessed.

    The number is composed of unique digits and does not start with zero.

    Returns:
        List[int]: A list of four unique integers.
    """
    digits = list(range(10))
    random.shuffle(digits)
    # Ensures the number does not start with zero
    if digits[0] == 0:
        digits[0], digits[1] = digits[1], digits[0]

    secret_number = digits[:4]
    return secret_number


def guessing_numbers(numbers_for_guessing: List[int]) -> int:
    """
    Runs the main game loop where the player guesses the number.

    The loop runs until the player guesses the correct number (4 "bulls").
    In each round, it evaluates the player's guess, prints the number
    of "bulls" and "cows", and counts the attempts.

    Args:
        numbers_for_guessing (List[int]): The list containing
        the secret number to be guessed.

    Returns:
        int: The total number of attempts the player needed.
    """
    attempt = 0
    while True:
        attempt += 1
        guessed_str = enter_guessed_numbers()
        guessed_ints = [int(digit) for digit in guessed_str]

        bulls = 0
        cows = 0

        for index, digit in enumerate(guessed_ints):
            if digit == numbers_for_guessing[index]:
                bulls += 1
            elif digit in numbers_for_guessing:
                cows += 1

        if bulls == 4:
            break

        bull_word, cow_word = get_correct_form_of_word(bulls, cows)
        print(f"{bulls} {bull_word}, {cows} {cow_word}")
        print(SEPARATOR_LINE)
    return attempt


def introductory_information() -> None:
    """
    Prints the introductory welcome message and game instructions.
    """
    print('\nHi there!')
    print(SEPARATOR_LINE)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print(SEPARATOR_LINE)
    print('Enter a number:')
    print(SEPARATOR_LINE)


def greeting(attempt: int) -> None:
    """
    Prints the final congratulatory message after the number is guessed.

    Args:
        attempt (int): The total number of attempts needed to win.
    """
    print("Correct, you've guessed the right number")
    print(f'in {attempt} guesses!')
    print(SEPARATOR_LINE)
    print("That's amazing!\n")


def main():
    """
    The main function that controls the entire program flow.

    It sequentially calls functions to display the intro, generate the number,
    run the game itself, and show the final greeting.
    """
    introductory_information()
    secret_number = generate_numbers_for_guessing()
    attempts_count = guessing_numbers(secret_number)
    greeting(attempts_count)


if __name__ == '__main__':
    main()