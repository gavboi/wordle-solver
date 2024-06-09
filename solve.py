from time import monotonic
from typing import List

from common import convert, get_args, LOGFILE, get_log_header


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
    total = len(words)
    t = monotonic()
    if total == 0:
        return ''
    letter_count = count_letters(words)
    word_coverage = []
    for w, word in enumerate(words):
        if monotonic() > t + 0.5:
            t = monotonic()
            print(f'Calculating guess: {round(100 * w / total)}%  ', end='\r')
        unique = []
        coverage = 0
        for letter in word:
            if letter not in unique:
                unique.append(letter)
                coverage += letter_count[convert(letter)]
        word_coverage.append(coverage)
    print(' '*40, end='\r')
    return words[word_coverage.index(max(word_coverage))]


def adjust_word_list(
        words: List[str], 
        guess: str, 
        feedback: str, 
        positioned: bool,
        debug: bool,
        file_debug: bool
) -> List[str]:
    start_length = len(words)
    t = monotonic()
    fp = None
    if file_debug: 
        fp = open(LOGFILE, 'a') 
    if positioned:
        for i in range(len(guess)):
            to_remove = []
            for w, word in enumerate(words):
                if monotonic() > t + 0.5:
                    t = monotonic()
                    numerator = i * start_length + w
                    print(f'Taking feedback: {round(100 * numerator / start_length)}%  ', end='\r')
                if feedback[i] == 'x':
                    if guess[i] in word:
                        debug_str = f'Excluding {word}: has {guess[i]}'
                        if debug:
                            print(debug_str)
                        if file_debug:
                            fp.write(debug_str + '\n')
                        to_remove.append(word)
                elif feedback[i] == 'c':
                    if guess[i] not in word:
                        debug_str = f'Excluding {word}: missing {guess[i]}'
                        if debug:
                            print(debug_str)
                        if file_debug:
                            fp.write(debug_str + '\n')
                        to_remove.append(word)
                    elif guess[i] == word[i]:
                        debug_str = f'Excluding {word}: {guess[i]} is index {i}'
                        if debug:
                            print(debug_str)
                        if file_debug:
                            fp.write(debug_str + '\n')
                        to_remove.append(word)
                elif feedback[i] == 'o':
                    if guess[i] != word[i]:
                        debug_str = f'Excluding {word}: index {i} not {guess[i]}'
                        if debug:
                            print(debug_str)
                        if file_debug:
                            fp.write(debug_str + '\n')
                        to_remove.append(word)
            words = [word for word in words if word not in to_remove]
    else:
        words_new = []
        for w, word in enumerate(words):
            exclude = False
            if monotonic() > t + 0.5:
                t = monotonic()
                print(f'Taking feedback: {round(100 * w / start_length)}%  ', end='\r')
            letters = list(word)
            for i in range(len(guess)):
                if guess[i] == word[i]:
                    letters[i] = '!'
                elif guess[i] in letters:
                    letters[letters.index(guess[i])] = '?'
            if letters.count('!') != feedback.count('o'):
                debug_str = f'Excluding {word}: exact count is {letters.count("!")} not {feedback.count("o")}'
                if debug:
                    print(debug_str)
                if file_debug:
                    fp.write(debug_str + '\n')
                exclude = True
            elif letters.count('?') != feedback.count('c'):
                debug_str = f'Excluding {word}: exact count is {letters.count("?")} not {feedback.count("c")}'
                if debug:
                    print(debug_str)
                if file_debug:
                    fp.write(debug_str + '\n')
                exclude = True
            if not exclude:
                words_new.append(word)
        words = words_new
    print(' '*40, end='\r')
    percent_removed = 100 * (start_length - len(words)) / start_length
    debug_str = f'{start_length} -> {len(words)}  |  {round(percent_removed,2)}% removed'
    if debug:
        print(debug_str)
    if file_debug:
        fp.write(debug_str + '\n')
        fp.close()
    return words


def main():
    # parse options
    args, words = get_args("Script will try and guess a Wordle word or Mastermind code.")
    
    # prep logfile
    if args.file_debug: 
        with open(LOGFILE, 'w') as fp: 
            fp.write(get_log_header())
    
    # pick guess
    feedback = ''
    guess = ''
    for g in range(args.guesses):
        first_guess = True
        while first_guess or feedback == 's' or feedback == 'skip': 
            first_guess = False
            guess = pick_word_simple(words)
            if guess == '':
                print_str = 'Something went wrong, no more possible guesses!'
                print(print_str)
                if args.file_debug: 
                    with open(LOGFILE, 'a') as fp: 
                        fp.write(print_str + '\n')
                return
            print_str = f'Guess {g+1}/{args.guesses}: {guess}'
            print(print_str)
            if args.file_debug: 
                with open(LOGFILE, 'a') as fp: 
                    fp.write(print_str + '\n')
            feedback = ''
            while len(feedback) != args.length and feedback not in ['s', 'skip']:
                feedback = input('Feedback: ')
            if args.file_debug: 
                with open(LOGFILE, 'a') as fp: 
                    fp.write(f'Feedback: {feedback}\n')
            if feedback == 'o' * args.length:
                print('Solved!')
                if args.file_debug: 
                    with open(LOGFILE, 'a') as fp: 
                        fp.write('Solved!\n')
                return
            elif feedback in ['s', 'skip']:
                words.remove(guess)
        words = adjust_word_list(words, guess, feedback, args.positioned, args.debug, args.file_debug)
    print('Failed solve!')
    if args.file_debug: 
        with open(LOGFILE, 'a') as fp: 
            fp.write(f'Failed solve!\n')


if __name__ == '__main__':
    main()
