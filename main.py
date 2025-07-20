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
    """
    Vyzve uživatele k zadání čísla a validuje vstup.

    Opakovaně se ptá na vstup, dokud uživatel nezadá platné 4místné číslo.
    Číslo musí obsahovat pouze číslice, nesmí začínat nulou a všechny
    číslice musí být unikátní.

    Returns:
        str: Zvalidovaný vstup od uživatele jako řetězec.
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
    Vrátí správné gramatické tvary slov "bull" a "cow".

    Args:
        bulls (int): Počet "býků" (správná číslice na správné pozici).
        cows (int): Počet "krav" (správná číslice na špatné pozici).

    Returns:
        Tuple[str, str]: Tuple se správnými tvary slov bull a cow.
    """
    bull_word = 'bull' if bulls == 1 else 'bulls'
    cow_word = 'cow' if cows == 1 else 'cows'
    return bull_word, cow_word

def generate_numbers_for_guessing() -> List[int]:
    """
    Vygeneruje náhodné 4místné tajné číslo pro hádání.

    Číslo je sestaveno z unikátních číslic a nezačíná nulou.

    Returns:
        List[int]: Seznam čtyř unikátních celých čísel.
    """
    digits = list(range(10))
    random.shuffle(digits)
    # Zajistí, aby číslo nezačínalo nulou
    if digits[0] == 0:
        digits[0], digits[1] = digits[1], digits[0]

    secret_number = digits[:4]
    return secret_number

def guessing_numbers(numbers_for_guessing: List[int]) -> int:
    """
    Spustí hlavní herní smyčku, kde hráč hádá číslo.

    Smyčka běží, dokud hráč neuhodne správné číslo (4 "býky").
    V každém kole vyhodnotí hráčův tip, vypíše počet "býků" a "krav"
    a počítá pokusy.

    Args:
        numbers_for_guessing (List[int]): Seznam s tajným číslem k uhodnutí.

    Returns:
        int: Celkový počet pokusů, které hráč potřeboval.
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
    Vypíše úvodní uvítací zprávu a instrukce ke hře.
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
    Vypíše závěrečnou gratulaci po uhodnutí čísla.

    Args:
        attempt (int): Celkový počet pokusů potřebných k vítězství.
    """
    print("Correct, you've guessed the right number")
    print(f'in {attempt} guesses!')
    print(SEPARATOR_LINE)
    print("That's amazing!\n")

def main():
    """
    Hlavní funkce, která řídí celý běh programu.

    Postupně volá funkce pro zobrazení úvodu, generování čísla,
    samotnou hru a závěrečnou gratulaci.
    """
    introductory_information()
    secret_number = generate_numbers_for_guessing()
    attempts_count = guessing_numbers(secret_number)
    greeting(attempts_count)

if __name__ == '__main__':
    main()
