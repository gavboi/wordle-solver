from common import get_all_words

from argparse import ArgumentParser as ap
import random
from typing import Tuple, List


def validate_guess(guess: str, target_word: str) -> Tuple[List[str]]:
    correct = []
    close = []
    wrong = []
    count = {}
    for letter in target_word:
        count[letter] = 1 if letter not in count else count[letter]+1
    for index, letter in enumerate(guess):
        if letter in target_word:
            if guess[index] == target_word[index]:
                correct.append(letter)
                if count[letter] == 0:
                    close.remove(letter)
                else:
                    count[letter] -= 1
            else:
                if count[letter] > 0:
                    close.append(letter)
                    count[letter] -= 1
        else:
            wrong.append(letter)
    return correct, close, wrong

def main():
    # parse options
    parser = ap(description='Try to guess the word the script chose.')
    parser.add_argument('-g', type=int, default=6, help='maximum guesses allowed')
    args = parser.parse_args()
    # read words
    all_words = get_all_words()

    # pick word
    target_word = random.choice(all_words)

    # play
    for g in range(args.g):
        guess = ''
        while len(guess) != 5:
            guess = input(f'Guess {g+1}: ')
        correct, close, wrong = validate_guess(guess, target_word)
        if len(correct) == 5:
            print('Yeehaw')
            break
        print(f'Correct: {",".join(correct)}')
        print(f'Close: {",".join(close)}')
        print(f'Wrong: {",".join(wrong)}')
        print('')

    print(f'The word was: {target_word}')

if __name__ == '__main__':
    main()
