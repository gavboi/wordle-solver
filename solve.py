from common import get_all_words, convert, adjust_word_list

import sys
from typing import List

def count_letters(words: List[str]) -> List[int]:
    letter_count = []
    for i in range(26):
        letter = convert(i)
        count = 0
        for word in words:
            if letter in word:
                count += 1
        letter_count.append(count)
    return letter_count

def pick_word_simple(words: List[str]) -> str:
    letter_count = count_letters(words)
    word_coverage = []
    for word in words:
        unique = []
        coverage = 0
        for letter in word:
            if letter not in unique:
                unique.append(letter)
                coverage += letter_count[convert(letter)]
        word_coverage.append(coverage)
    return words[word_coverage.index(max(word_coverage))]


def main():
    # parse options
    guess_count = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    # read words and other setup
    words = get_all_words()
    word_count = len(words)
    # pick guess
    for g in range(guess_count):
        guess = pick_word_simple(words)
        print(guess)
        feedback = input('Feedback: ')
        if feedback == 'ooooo':
            print('Solved!')
            return
        words = adjust_word_list(words, guess, feedback, debug=True)
    print('Failed solve!')

if __name__ == '__main__':
    main()
