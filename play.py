from common import get_all_words, validate_guess

import random
import sys

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
