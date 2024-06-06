from common import get_all_words, convert, get_all_mastermind

from argparse import ArgumentParser as ap
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
    if len(words) == 0:
        return None
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

def adjust_word_list(
        words: List[str], 
        guess: str, 
        feedback: str, 
        ans_len: str,
        positioned: bool,
        debug: bool,
) -> None:
    start_length = len(words)
    if positioned:
        for i in range(ans_len):
            to_remove = []
            for word in words:
                if feedback[i] == 'x':
                    if guess[i] in word:
                        if debug: print(f'Excluding {word}: has {guess[i]}')
                        to_remove.append(word)
                elif feedback[i] == 'c':
                    if guess[i] not in word:
                        if debug: print(f'Excluding {word}: missing {guess[i]}')
                        to_remove.append(word)
                    elif guess[i] == word[i]:
                        if debug: print(f'Excluding {word}: {guess[i]} is index {i}')
                        to_remove.append(word)
                elif feedback[i] == 'o':
                    if guess[i] != word[i]:
                        if debug: print(f'Excluding {word}: index {i} not {guess[i]}')
                        to_remove.append(word)
            words = [word for word in words if word not in to_remove]
    else:
        to_remove = []
        for word in words:
            letters = list(word)
            for i in range(ans_len):
                if guess[i] == word[i]:
                    letters[i] = '!'
                elif guess[i] in letters:
                    letters[letters.index(guess[i])] = '?'
            if letters.count('!') != feedback.count('o'):
                if debug: print(f'Excluding {word}: exact count is {letters.count("!")} not {feedback.count('o')}')
                to_remove.append(word)
            elif letters.count('?') != feedback.count('c'):
                if debug: print(f'Excluding {word}: exact count is {letters.count("?")} not {feedback.count('c')}')
                to_remove.append(word)
        words = [word for word in words if word not in to_remove]
    percent_removed = 100 * (start_length - len(words)) / start_length
    if debug: print(f'{start_length} -> {len(words)}  |  {round(percent_removed,2)}% removed')
    return words


def main():
    # parse options
    parser = ap(description='Suggests guesses for Wordle or Mastermind.')
    parser.add_argument('-m', '--mastermind', nargs='?', type=int, const=8, default=None, metavar='OPTIONS', help='set game type to mastermind, optionally provide amount of options per index (default 8)')
    parser.add_argument('-g', '--guesses', type=int, default=None, metavar='COUNT', help='maximum guesses allowed (default 6 for wordle, 10 for mastermind)')
    parser.add_argument('-l', '--length', type=int, default=None, help='length of correct answer (default 5 for wordle, 4 for mastermind)')
    parser.add_argument('-p', '--positioned', default=None, choices=['true', 'false'], help='whether feedback position matters (default True for wordle, False for mastermind)')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='enable debug prints (default False)')
    args = parser.parse_args()
    # use default guesses wordle = 6, mastermind = 10 if no count provided
    if args.guesses == None:
        guesses = 6 if args.mastermind == None else 10
    else:
        guesses = args.guesses
    # use default lengths wordle = 5, mastermind = 4 if no length provided
    if args.length == None:
        ans_len = 5 if args.mastermind == None else 4
    else:
        ans_len = args.length
    # use default lengths wordle = 5, mastermind = 4 if no length provided
    if args.positioned == None:
        positioned = True if args.mastermind == None else False
    else:
        positioned = args.positioned
    # set word list to mastermind or wordle ones accordingly
    if args.mastermind != None:
        words = get_all_mastermind(args.mastermind, ans_len)
    else:
        if ans_len == 5:
            words = get_all_words()
        else:
            raise NotImplementedError(f'No word list found for length {ans_len}')
    word_count = len(words)
    # pick guess
    for g in range(guesses):
        first_guess = True
        while first_guess or feedback == 's' or feedback == 'skip': 
            first_guess = False
            guess = pick_word_simple(words)
            if guess == None:
                print('Something went wrong, no more possible guesses!')
                return
            print(f'Guess {g+1}/{guesses}: {guess}')
            feedback = ''
            while len(feedback) != ans_len and feedback not in ['s', 'skip']:
                feedback = input('Feedback: ')
            if feedback == 'o'*ans_len:
                print('Solved!')
                return
            elif feedback in ['s', 'skip']:
                words.remove(guess)
        words = adjust_word_list(words, guess, feedback, ans_len, positioned, args.debug)
    print('Failed solve!')

if __name__ == '__main__':
    main()
