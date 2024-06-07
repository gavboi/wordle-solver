from common import convert, get_args

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
        positioned: bool,
        debug: bool,
) -> None:
    start_length = len(words)
    if positioned:
        for i in range(len(guess)):
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
            for i in range(len(guess)):
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
    args, words = get_args("Script will try and guess a Wordle word or Mastermind code.")
    
    # pick guess
    for g in range(args.guesses):
        first_guess = True
        while first_guess or feedback == 's' or feedback == 'skip': 
            first_guess = False
            guess = pick_word_simple(words)
            if guess == None:
                print('Something went wrong, no more possible guesses!')
                return
            print(f'Guess {g+1}/{args.guesses}: {guess}')
            feedback = ''
            while len(feedback) != args.length and feedback not in ['s', 'skip']:
                feedback = input('Feedback: ')
            if feedback == 'o' * args.length:
                print('Solved!')
                return
            elif feedback in ['s', 'skip']:
                words.remove(guess)
        words = adjust_word_list(words, guess, feedback, args.positioned, args.debug)
    print('Failed solve!')

if __name__ == '__main__':
    main()
