# WordleHelper
A program that helps you solve Wordle, by giving you suggested words to use based on previous guesses.

The program's main loop starts with the user inputting their latest guess, and the result. The program then goes
through the list of possible guesses, and removes any that don't fit with the information provided. After it
has a new, updated list of possible guesses, it analyzes the frequency with which each letter appears, and provides a
suggested next guess based on that (the suggested guess has the most commonly used letters among the remaining possible
answers, and no duplicate letters if possible, so even if the guess is wrong, the guess is likely to eliminate a
significant number of possible guesses).

The datasets used in this program are the list of valid guess words (which does not include answers), and the list of possible answers for the popular
word game Wordle. The lists came from  GitHub user cfreshman, you can find them here:

Guesses: https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c

Answers: https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
