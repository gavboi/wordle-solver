# Wordle Solver
Provides good guesses for Wordles. CLI.

## Usage

### Playing
Run `play.py` to play a wordle. Provide a positive numerical option to set a custom guess counter. 

### Solving
Run `solve.py` to have words suggested to you for playing a puzzle somewhere else, or to have it play against you. Provide a positive numerical option to set a custom guess counter. When it asks for feedback, `x` means a letter is not present, `c` means it is present but in the wrong spot, and `o` means it is correct. For example, if the word is `bread` and the guess is `train`, the feedback would be `xocxx` (`t` is not present, `r` is correct, `a` is present elsewhere in the word, and `i` and `n` are not present).

## Notes

### Solving Algorithm Choices

- Words are chosen that contain letters that are each in as many words as possible. It does not prioritize different letters to get the most overall word coverage. 














