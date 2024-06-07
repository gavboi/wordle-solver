from common import get_args

import random


def validate_guess(guess: str, target_word: str, positioned: bool) -> str:
    feedback = []
    target_list = list(target_word)
    for i in range(len(guess)):
        if guess[i] == target_list[i]:
            feedback.append('o')
            target_list[i] = '_'
        else:
            feedback.append('x')
    for i in range(len(guess)):
        if feedback[i] == 'x' and guess[i] in target_list:
            feedback[i] = 'c'
            target_list[target_list.index(guess[i])] = '_'
    if positioned:
        feedback_final = ''.join(feedback)
    else:
        feedback_final = ''
        for letter in ['o', 'c', 'x']:
            feedback_final += letter * feedback.count(letter)
    return feedback_final

def main():
    # parse args
    args, words = get_args("Try to guess the Wordle word or Mastermind code the script comes up with.")

    # pick word
    target_word = random.choice(words)

    # play
    for g in range(args.guesses):
        guess = ''
        while guess not in words:
            guess = input(f'Guess {g+1}/{args.guesses}: ')
        feedback = validate_guess(guess, target_word, args.positioned)
        if feedback == 'o' * len(target_word):
            print('You guessed the word!')
            break
        else:
            print(feedback)

    print(f'The word was: {target_word}')

if __name__ == '__main__':
    main()
