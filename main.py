
import tkinter as tk


ANSWERS = "wordle-answers-alphabetical.txt"     # https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
GUESSES = "wordle-allowed-guesses.txt"          # https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c
GRAY = "#787C7E"
YELLOW = "#C9B458"
GREEN = "#6AAA64"


# arguments: the word guessed by the user, the pattern of green/yellow/black squares provided by the game, and the list
#   of words being filtered
# returns: None
def filter_words(wor, pat, word_list):
    c = ['_', '_', '_', '_', '_']       # This first block of code figures out where each letter in the provided
    u = ['_', '_', '_', '_', '_']       # word is or is not in the answer word, based on the pattern provided
    deconfirmed = ""
    dups_dic = {}
    dup_check = ''
    if len(set(wor)) < 5:
        for i in range(5):
            if pat[i] != 'b':
                if wor[i] in dups_dic.keys():
                    dups_dic[wor[i]] += 1
                    dup_check += wor[i]
                else:
                    dups_dic[wor[i]] = 1
    for i in range(5):
        if pat[i] == 'g':
            c[i] = wor[i]
        if pat[i] == 'y':
            u[i] = wor[i]
        if pat[i] == 'b':
            if wor[i] not in c and wor[i] not in u and wor[i] not in wor[:i] and wor[i] not in wor[i+1:]:
                deconfirmed += wor[i]
    confirmed = "".join(c)
    unconfirmed = "".join(u)
    deconfirmed += '_' * (5-len(deconfirmed))

    i = 0
    while i < len(word_list):                                       # the second code block does the actual filtering
        for j in range(5):
            if confirmed[j] != '_' and word_list[i][j] != confirmed[j]:     # if there are letters which have confirmed
                word_list.remove(word_list[i])                              # positions in the answer, and the correct
                i -= 1                                                      # letter is not in that position in the
                break                                                       # guess word, the word is removed
            if unconfirmed[j] != '_':
                if word_list[i][j] == unconfirmed[j]:                       # if there are letters which are in the
                    word_list.remove(word_list[i])                          # answer, but their position is unknown,
                    i -= 1                                                  # the guess word is removed if the guess
                    break                                                   # word has that letter in the position it is
                if unconfirmed[j] not in word_list[i]:                      # confirmed not to be in the answer, or if
                    word_list.remove(word_list[i])                          # the word does not contain that letter
                    i -= 1
                    break
            if deconfirmed[j] != '_' and deconfirmed[j] in word_list[i]:    # if there are letters which are confirmed
                word_list.remove(word_list[i])                              # not to be in the answer, and the guess
                i -= 1                                                      # word contains any of those letters, the
                break                                                       # guess word is removed
            if word_list[i][j] in dup_check:                                            # if the letter being examined
                if word_list[i].count(word_list[i][j]) < dups_dic[word_list[i][j]]:     # is a duplicate letter in the
                    word_list.remove(word_list[i])                                      # answer, but not in the guess
                    i -= 1                                                              # word, the word is removed
                    break
            if dup_check == '' and word_list[i][j] in dups_dic.keys() and word_list[i].count(word_list[i][j]) > 1:
                word_list.remove(word_list[i])                  # if the letter being examined is a duplicate in the
                i -= 1                                          # guess word, but is confirmed to not be a duplicate
                break                                           # in the answer, the word is removed
        i += 1


# arguments: the list of words to be analyzed
# returns: a dictionary where each key is a letter of the english alphabet, and the value is a list consisting of the
#   number of times the letter appeared in the provided list, and the number of times it appeared in each position in
#   the word (ex. lf['a'] = [3, 0, 2, 0, 0, 1] means that 'a' appeared 3 times overall, twice as the second letter in
#   a word, and once as the fifth letter in a word)
def frequency_analysis(wl):
    lf = {}                                         # letter frequency dictionary to be returned
    for i in range(0, 26):                          # initialize the dictionary with each letter as a key
        lf[chr(97 + i)] = [0, 0, 0, 0, 0, 0]
    for word in wl:                                 # tally up the letter frequencies
        for i in range(5):
            letter = word[i]
            lf[letter][0] += 1
            lf[letter][i+1] += 1
    return lf


def click1(event):
    color = b1["bg"]
    if color == GRAY:
        b1["bg"] = YELLOW
    elif color == YELLOW:
        b1["bg"] = GREEN
    elif color == GREEN:
        b1["bg"] = GRAY


def click2(event):
    color = b2["bg"]
    if color == GRAY:
        b2["bg"] = YELLOW
    elif color == YELLOW:
        b2["bg"] = GREEN
    elif color == GREEN:
        b2["bg"] = GRAY


def click3(event):
    color = b3["bg"]
    if color == GRAY:
        b3["bg"] = YELLOW
    elif color == YELLOW:
        b3["bg"] = GREEN
    elif color == GREEN:
        b3["bg"] = GRAY


def click4(event):
    color = b4["bg"]
    if color == GRAY:
        b4["bg"] = YELLOW
    elif color == YELLOW:
        b4["bg"] = GREEN
    elif color == GREEN:
        b4["bg"] = GRAY


def click5(event):
    color = b5["bg"]
    if color == GRAY:
        b5["bg"] = YELLOW
    elif color == YELLOW:
        b5["bg"] = GREEN
    elif color == GREEN:
        b5["bg"] = GRAY


def callback(*args):
    result = entry.get().upper()
    result = result + (' '*(5-len(result)))
    b1["text"] = result[0]
    b2["text"] = result[1]
    b3["text"] = result[2]
    b4["text"] = result[3]
    b5["text"] = result[4]


def sub(event):
    result = entry.get()
    colors = [b1["bg"], b2["bg"], b3["bg"], b4["bg"], b5["bg"]]
    for i in range(5):
        if colors[i] == GRAY:
            colors[i] = 'b'
        elif colors[i] == YELLOW:
            colors[i] = 'y'
        elif colors[i] == GREEN:
            colors[i] = 'g'
    filter_words(result, colors, guess_list)  # filter words that are no longer viable
    filter_words(result, colors, answer_list)
    suggestions = guess_list.copy()
    letter_frequency = frequency_analysis(guess_list)
    best_score = 0
    if len(suggestions) > 8:  # unless we're down to a few possible solutions,
        for i in guess_list:  # remove words with duplicate letters
            if len(set(i)) < 5:
                suggestions.remove(i)
    if len(suggestions) == 0:  # if all viable answers contain duplicate letters, the list of suggestions resets
        suggestions = guess_list.copy()
    for i in suggestions:
        score = 0
        if i in answer_list:
            score += 50  # guess words in the answer list are more heavily weighted when fewer guess words remain
        for j in range(5):
            score += letter_frequency[i[j]][j + 1]  # this is equivalent to the % frequency with which the letter
        if score > best_score:  # is in a given position multiplied by the number of times
            best_score = score  # the letter appears in the word list
            suggestion = i
    sug["text"] = suggestion.upper()


if __name__ == '__main__':
    obj = open(ANSWERS)  # initialize list of answers
    answer_list = obj.readlines()
    obj.close()
    obj = open(GUESSES)  # initialize list of guesses
    guess_list = obj.readlines()
    obj.close()
    for i in range(len(guess_list) - 1):  # strip each word of the newline character
        guess_list[i] = guess_list[i][:-1]  # (the last word does not have a newline character)
    for i in range(len(answer_list) - 1):  # strip each word of the newline character, and add the
        answer_list[i] = answer_list[i][:-1]  # list of answers to the list of possible guesses
        guess_list.append(answer_list[i])

    window = tk.Tk()
    window.title("Wordle Helper")
    window.geometry("600x350")
    window.grid_columnconfigure((0, 6), weight=1)
    b1 = tk.Button(
        width=3,
        height=1,
        bg=GRAY,
        fg="white",
        master=window,
        font="Helvetica 18 bold"
    )
    b2 = tk.Button(
        width=3,
        height=1,
        bg=GRAY,
        fg="white",
        master=window,
        font="Helvetica 18 bold"
    )
    b3 = tk.Button(
        width=3,
        height=1,
        bg=GRAY,
        fg="white",
        master=window,
        font="Helvetica 18 bold"
    )
    b4 = tk.Button(
        width=3,
        height=1,
        bg=GRAY,
        fg="white",
        master=window,
        font="Helvetica 18 bold"
    )
    b5 = tk.Button(
        width=3,
        height=1,
        bg=GRAY,
        fg="white",
        master=window,
        font="Helvetica 18 bold"
    )
    b1.bind("<Button-1>", click1)
    b2.bind("<Button-1>", click2)
    b3.bind("<Button-1>", click3)
    b4.bind("<Button-1>", click4)
    b5.bind("<Button-1>", click5)
    b1.grid(row=0, column=1, padx=1, pady=30)
    b2.grid(row=0, column=2, padx=1, pady=30)
    b3.grid(row=0, column=3, padx=1, pady=30)
    b4.grid(row=0, column=4, padx=1, pady=30)
    b5.grid(row=0, column=5, padx=1, pady=30)
    var = tk.StringVar()
    entry = tk.Entry(fg="black", bg="white", width=15, textvariable=var)
    entry.grid(row=1, column=2, pady=5, columnspan=3)
    var.trace("w", callback)
    submit = tk.Button(
        text="submit",
        width=8,
        height=1,
        bg=GRAY,
        fg="black",
        master=window)
    submit.bind("<Button-1>", sub)
    submit.grid(row=2, column=2, columnspan=3)
    sug = tk.Label(text='Please enter your guess.')
    sug.grid(row=3, column=2, columnspan=3, pady=15)
    window.mainloop()
