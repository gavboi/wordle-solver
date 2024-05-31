from common import get_all_words

import random
import sys


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
    guess_count = int(sys.argv[1]) if len(sys.argv) > 1 else 6

    # read words
    all_words = get_all_words()

    # pick word
    target_word = random.choice(all_words)

    # play
    for g in range(guess_count):
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
