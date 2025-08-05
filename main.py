"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Josef Nuhlíček
email: josef.nuhlicek@gmail.com
"""

"""Bulls and Cows game with persistent statistics and timers.

This script allows a user to play the classic "Bulls and Cows" number
guessing game. It tracks the number of attempts and the time taken for
each game, saving these statistics to a local file.
"""

import random
import time
from pathlib import Path
from typing import List, Optional, Tuple

# --- Configuration Constants ---
# The number of digits in the secret number.
# Changing this value will adjust the entire game's logic.
DIGIT_COUNT = 4

# The separator line for better console output
SEPARATOR_LINE = '-' * 47

# --- Path Constants ---
# This ensures the stats file is always in the same directory as the script,
# making the application portable.
SCRIPT_DIR = Path(__file__).resolve().parent
STATS_FILENAME = "bulls_and_cows_stats.txt"
STATS_FILE_PATH = SCRIPT_DIR / STATS_FILENAME


# --- Utility Functions ---

def get_correct_form_of_word(count: int, word: str) -> str:
    """Returns the correct plural form of a word based on the count.

    Example:
        >>> get_correct_form_of_word(1, "bull")
        'bull'
        >>> get_correct_form_of_word(2, "bull")
        'bulls'

    Args:
        count: The number to determine if the word should be plural.
        word: The singular form of the word.

    Returns:
        The correctly pluralized word as a string.
    """
    return word if count == 1 else f"{word}s"


def format_duration(total_seconds: float) -> str:
    """Converts a duration in seconds to a human-readable string.

    Formats the duration as "X minutes and Y seconds" if it is over
    60 seconds, otherwise shows it as "Z.ZZ seconds".

    Args:
        total_seconds: The duration in seconds.

    Returns:
        A formatted, human-readable string representing the duration.
    """
    if total_seconds < 60:
        return f"{total_seconds:.2f} seconds"

    minutes, seconds = divmod(total_seconds, 60)
    minutes = int(minutes)
    seconds = int(seconds)

    minute_str = get_correct_form_of_word(minutes, "minute")
    second_str = get_correct_form_of_word(seconds, "second")

    return f"{minutes} {minute_str} and {seconds} {second_str}"


def display_stats(stats: List[Tuple[int, float]]) -> None:
    """Displays formatted game statistics to the console.

    Args:
        stats: A list of tuples, where each tuple contains the
            number of attempts (int) and duration (float) for a game.
    """
    print("\n--- Game Statistics ---")
    if not stats:
        print("No games played yet.")
        return

    attempts_list = [s[0] for s in stats]
    duration_list = [s[1] for s in stats]
    game_count = len(stats)

    avg_guesses = sum(attempts_list) / game_count
    avg_duration = sum(duration_list) / game_count

    fastest_game_str = format_duration(min(duration_list))
    avg_duration_str = format_duration(avg_duration)

    print(f"Total games played: {game_count}")
    print(f"Best score (least guesses): {min(attempts_list)}")
    print(f"Fastest game: {fastest_game_str}")
    print(f"Average guesses per game: {avg_guesses:.2f}")
    print(f"Average time per game: {avg_duration_str}")
    print("-----------------------")


# --- Game Class ---

class Game:
    """Encapsulates all logic and state for a single Bulls and Cows game.

    This class manages the secret number, tracks attempts, and runs the
    gameplay loop for a single session.

    Attributes:
        digits: The number of digits in the secret number.
        secret_number: The generated secret number for the current game.
        attempts: The current number of attempts in this game session.
        start_time: The monotonic time when the game started.
    """

    def __init__(self, digits: int = DIGIT_COUNT):
        """Initializes a new Game instance.

        Args:
            digits: The number of digits for the secret number.
                Defaults to the global DIGIT_COUNT.
        """
        self.digits = digits
        self.secret_number: List[int] = self._generate_secret_number()
        self.attempts: int = 0
        self.start_time: float = 0.0

    def _generate_secret_number(self) -> List[int]:
        """Generates a random secret number with unique digits.

        Returns:
            A list of unique integers representing the secret number.

        Raises:
            ValueError: If the requested number of digits is greater than 10,
                as unique digits are required.
        """
        if self.digits > 10:
            raise ValueError(
                "Cannot generate a number with more than 10 unique digits."
            )

        all_digits = list(range(10))
        random.shuffle(all_digits)

        # Ensure the number doesn't start with zero if it's multi-digit.
        if self.digits > 1 and all_digits[0] == 0:
            all_digits[0], all_digits[1] = all_digits[1], all_digits[0]

        return all_digits[:self.digits]

    def _validate_guess(self, guess: str) -> Optional[str]:
        """Validates the player's guess string.

        Args:
            guess: The player's guess received as a string.

        Returns:
            None if the guess is valid, otherwise a string
            with the specific error message.
        """
        if not guess.isdigit():
            return "Input must contain only digits."
        if len(guess) != self.digits:
            return f"Input must be exactly {self.digits} digits long."
        if self.digits > 1 and guess[0] == '0':
            return "The number must not start with zero."
        if len(set(guess)) != self.digits:
            return f"The number must contain {self.digits} unique digits."
        return None

    def _get_player_guess(self) -> List[int]:
        """Prompts the player for input until a valid guess is provided.

        Returns:
            The validated player's guess as a list of integers.
        """
        while True:
            guess_str = input(">>> ").strip()
            error = self._validate_guess(guess_str)
            if error:
                print(f"Invalid input: {error} Please try again.")
            else:
                return [int(digit) for digit in guess_str]

    def _evaluate_guess(self, guess: List[int]) -> Tuple[int, int]:
        """Compares a guess against the secret number.

        Example:
            If `self.secret_number` is `[1, 2, 3, 4]`, then:
            `_evaluate_guess([1, 2, 4, 3])` would return `(2, 2)`.

        Args:
            guess: The player's guess as a list of integers.

        Returns:
            A tuple containing the number of bulls and cows.
        """
        bulls = sum(s == g for s, g in zip(self.secret_number, guess))
        common_digits = set(self.secret_number) & set(guess)
        cows = len(common_digits) - bulls
        return bulls, cows

    def play(self) -> Tuple[int, float]:
        """Runs the main game loop for a single session.

        Returns:
            A tuple containing the total number of attempts and the
            total duration in seconds for the game.
        """
        print('\nHi there!')
        print(SEPARATOR_LINE)
        print(f"I've generated a random {self.digits} digit number for you.")
        print("Let's play a bulls and cows game!")
        print(SEPARATOR_LINE)
        print('Enter a number:')
        print(SEPARATOR_LINE)

        # Use monotonic clock for reliable duration measurement.
        self.start_time = time.monotonic()

        while True:
            self.attempts += 1
            print(f"Attempt #{self.attempts}")
            guess = self._get_player_guess()

            bulls, cows = self._evaluate_guess(guess)

            if bulls == self.digits:
                end_time = time.monotonic()
                duration = end_time - self.start_time
                secret_str = "".join(map(str, self.secret_number))
                formatted_duration = format_duration(duration)

                print(f"\nCorrect, you've guessed {secret_str} in "
                      f"{self.attempts} attempts.")
                print(f"This game took you {formatted_duration}.")
                return self.attempts, duration

            bull_word = get_correct_form_of_word(bulls, "bull")
            cow_word = get_correct_form_of_word(cows, "cow")
            print(f"Result: {bulls} {bull_word}, {cows} {cow_word}")
            print(SEPARATOR_LINE)


# --- Main Application Logic ---

def load_stats() -> List[Tuple[int, float]]:
    """Loads game scores from the stats file.

    If the file does not exist, it returns an empty list. It safely
    skips any malformed lines in the file.

    Returns:
        A list of tuples, where each tuple contains the number of
        attempts (int) and duration (float) for a completed game.
    """
    if not STATS_FILE_PATH.exists():
        return []

    stats = []
    with open(STATS_FILE_PATH, "r") as f:
        for line in f:
            try:
                attempts_str, duration_str = line.strip().split(',')
                stats.append((int(attempts_str), float(duration_str)))
            except (ValueError, IndexError):
                # Ignore malformed lines to prevent crashes.
                pass
    return stats


def save_stats(stats: List[Tuple[int, float]]) -> None:
    """Saves a list of scores to the stats file.

    This will overwrite the existing file with the new list of scores.

    Args:
        stats: The list of score tuples to save.
    """
    with open(STATS_FILE_PATH, "w") as f:
        for attempts, duration in stats:
            f.write(f"{attempts},{duration}\n")


def main():
    """The main entry point for the application.

    Manages the overall application flow, including loading and displaying
    stats, running game sessions in a loop, and saving stats after
    each game.
    """
    print("\nWelcome to Bulls and Cows!")

    stats = load_stats()
    display_stats(stats)

    while True:
        game = Game(digits=DIGIT_COUNT)
        final_attempts, game_duration = game.play()

        stats.append((final_attempts, game_duration))
        save_stats(stats)

        display_stats(stats)

        prompt = "\nPlay again? (y/n): "
        play_again = input(prompt).strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break


if __name__ == '__main__':
    main()
