"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Josef Nuhlíček
email: josef.nuhlicek@gmail.com
"""
import random
from typing import List, Tuple

# Oddělovací čára pro výpis do konzole
SEPARATOR_LINE = '-' * 47

def enter_guessed_numbers() -> str:
    """_summary_

    Returns:
        str: _description_
    """    
    
    is_guessed_number_ok = False

    while not is_guessed_number_ok:
        guessed_numbers = input(">>> ").strip()
        if not guessed_numbers.isdigit():
            print('The entered string contains a non-numeric character, ' \
            'try again.')
        elif len(guessed_numbers) < 4:
            print('The entered number is less than 4 digits, try again.')
        elif len(guessed_numbers) > 4:
            print('The entered number is longer than 4 digits, try again.')
        elif guessed_numbers[0] == '0':
            print('The entered number starts with zero, try again.')
        elif len(set(guessed_numbers)) < 4:
            print('TThe entered number contains duplicates, try again.')
        else:
            is_guessed_number_ok = True         
    
    return guessed_numbers

def get_correct_form_of_word(bulls: int, cows: int) -> Tuple[str, str]:
    """_summary_

    Args:
        bulls (int): _description_
        cows (int): _description_

    Returns:
        Tuple[str, str]: _description_
    """    
    bull_word = 'bull' if bulls == 1 else 'bulls'
    cow_word = 'cow' if cows == 1 else 'cows'
    return bull_word, cow_word

def generate_numbers_for_guessing() -> List[int]:
    """_summary_

    Returns:
        List[int]: _description_
    """   
    digits = list(range(10))
    random.shuffle(digits)
    if digits[0] == 0:
        digits[0], digits[1] = digits[1], digits[0]
    
    secret_number = digits[:4]
    # print(f"Secret number for testing: {secret_number}") # Ponechat jen pro ladění
    return secret_number

def guessing_numbers(numbers_for_guessing: List[int]) -> int:
    """_summary_

    Args:
        numbers_for_guessing (List[int]): _description_

    Returns:
        int: _description_
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
    """_summary_
    """    
    print('\nHi there!')
    print(SEPARATOR_LINE)
    print('I\'ve generated a random 4 digit number for you.')
    print('Let\'s play a bulls and cows game.')
    print(SEPARATOR_LINE)
    print('Enter a number:')
    print(SEPARATOR_LINE)

def greeting(attempt: int) -> None:
    """_summary_

    Args:
        attempt (int): _description_
    """    
    print('Correct, you\'ve guessed the right number')
    print(f'in {attempt} guesses!')
    print(SEPARATOR_LINE)
    print('That\'s amazing!\n')

def main():
    """_summary_
    """    
    introductory_information()
    secret_number = generate_numbers_for_guessing()
    attempts_count = guessing_numbers(secret_number)
    greeting(attempts_count)

if __name__ == '__main__':
    main()
