# Wordle Solver
Provides good guesses for Wordles and Mastermind. CLI.

## Usage

### Playing
Run `play.py` to play a simple Wordle (currently does not support Mastermind). 

#### Options
- `-g INT`: sets a custom guess counter

### Solving
Run `solve.py` to have words suggested to you for playing a Wordle or Mastermind somewhere else, or to have it play against you. 

When it asks for feedback, `x` means a letter is not present, `c` means it is present but in the wrong spot, and `o` means it is correct. For example, if the word is `bread` and the guess is `train`, the feedback would be `xocxx` (`t` is not present, `r` is correct, `a` is present elsewhere in the word, and `i` and `n` are not present). 

If position is set to not matter, the order of feedback does not matter (the feedback from above could be given as `ocxxx`).

#### Options
- `-h`: shows help message
- `-m [INT]`: switches game from Wordle to Mastermind; value sets amount of options
- `-g INT`: sets a custom guess counter
- `-l INT`: sets length of word/code
- `-p BOOL`: sets whether positon of feedback matters
- `-d`: enables debug prints

## Notes

The word list included contains around 5500 words, and contains some that are not used by NY Times. Feel free to add or remove words from the list as you want/need to. 

### Solving Algorithm Choices

- Words are chosen that contain letters that are each in as many words as possible. It does not prioritize different letters to get the most overall word coverage. It is likely more effective for Mastermind than Wordle, but still does well enough. 














