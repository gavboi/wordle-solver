from typing import List, Union, Tuple

import argparse

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

def get_args(description: str) -> Tuple[argparse.Namespace, List[str]]:
    # parse options
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-m', '--mastermind', nargs='?', type=int, const=8, default=None, metavar='OPTIONS', help='set game type to mastermind, optionally provide amount of options per index (default 8)')
    parser.add_argument('-g', '--guesses', type=int, default=None, metavar='COUNT', help='maximum guesses allowed (default 6 for wordle, 10 for mastermind)')
    parser.add_argument('-l', '--length', type=int, default=None, help='length of correct answer (default 5 for wordle, 4 for mastermind)')
    parser.add_argument('-p', '--positioned', default=None, choices=['true', 'false'], help='whether feedback position matters (default True for wordle, False for mastermind)')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='enable debug prints (default False)')
    args = parser.parse_args()
    # use default guesses wordle = 6, mastermind = 10 if no count provided
    if args.guesses == None:
        args.guesses = 6 if args.mastermind == None else 10
    # use default lengths wordle = 5, mastermind = 4 if no length provided
    if args.length == None:
        args.length = 5 if args.mastermind == None else 4
    # use default lengths wordle = 5, mastermind = 4 if no length provided
    if args.positioned == None:
        args.positioned = True if args.mastermind == None else False
    else:
        args.positioned = True if args.positioned == 'true' else False
    # set word list to mastermind or wordle ones accordingly
    if args.mastermind != None:
        words = get_all_mastermind(args.mastermind, args.length)
    else:
        if args.length == 5:
            words = get_all_words()
        else:
            raise NotImplementedError(f'No word list found for length {args.length}')
    if args.debug: print(f'm:{args.mastermind} g:{args.guesses} l:{args.length} p:{args.positioned}')
    return args, words
