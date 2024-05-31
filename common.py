from typing import List, Tuple, Union

def get_all_words() -> List[str]:
    with open('five_letter_words.txt', 'r') as file:
        all_words = file.readlines()
    all_words = [word.strip() for word in all_words]
    return all_words

def get_all_mastermind(options: int = 6, length: int = 4) -> List[str]:
    all_codes = []
    for n in range(options ** length):
        code = ''
        for i in range(length - 1, -1, -1):
            code = code + convert(n // (options ** i))
            n = n % (options ** i)
        all_codes.append(code)
    return all_codes

def convert(arg: Union[str, int]) -> Union[str, int]:
    if type(arg) is str:
        if len(arg) > 1:
            raise ValueError(f'Arg {arg} is not length 1')
        return ord(arg.lower()) - ord('a')
    elif type(arg) is int:
        if arg >= 26 or arg < 0:
            raise ValueError(f'Arg {arg} must be within the length of alphabet')
        return chr(arg + ord('a'))
