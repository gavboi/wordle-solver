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
        if arg >= 26 or arg < 0:
            raise ValueError(f'Arg {arg} must be within the length of alphabet')
        return chr(arg + ord('a'))

def adjust_word_list(words: List[str], guess: str, feedback: str, debug: bool = False) -> None:
    start_length = len(words)
    for i in range(5):
        to_remove = []
        for word in words:
            exclude = False
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
    percent_removed = 100 * (start_length - len(words)) / start_length
    if debug: print(f'{start_length} -> {len(words)}  |  {round(percent_removed,2)}% removed')
    return words
