from typing import List, Tuple, Union

def get_all_words() -> List[str]:
    with open('five_letter_words.txt', 'r') as file:
        all_words = file.readlines()
    all_words = [word.strip() for word in all_words]
    return all_words

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

def convert(arg: Union[str, int]) -> Union[str, int]:
    if type(arg) is str:
        if len(arg) > 1:
            raise ValueError(f'Arg {arg} is not length 1')
        return ord(arg.lower()) - ord('a')
    elif type(arg) is int:
        if int >= 26 or int < 0:
            raise ValueError(f'Arg {arg} must be within the length of alphabet')
        return chr(arg + ord('a'))
