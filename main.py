
ANSWERS = "wordle-answers-alphabetical.txt"     # https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
GUESSES = "wordle-allowed-guesses.txt"          # https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c


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


if __name__ == '__main__':
    obj = open(ANSWERS)             # initialize list of answers
    answer_list = obj.readlines()
    obj.close()
    obj = open(GUESSES)             # initialize list of guesses
    guess_list = obj.readlines()
    obj.close()
    for i in range(len(guess_list)-1):              # strip each word of the newline character
        guess_list[i] = guess_list[i][:-1]          # (the last word does not have a newline character)
    for i in range(len(answer_list)-1):         # strip each word of the newline character, and add the
        answer_list[i] = answer_list[i][:-1]    # list of answers to the list of possible guesses
        guess_list.append(answer_list[i])

    print('Welcome to Wordle Helper!')
    while True:
        word = input('What was your guess?\n').lower()
        pattern = input('What was the color pattern? For example, if the first letter was green, the second was yellow,'
                        ' and the other three were black, you would type GYBBB:\n').lower()
        filter_words(word, pattern, guess_list)     # filter words that are no longer viable
        filter_words(word, pattern, answer_list)
        suggestions = guess_list.copy()
        letter_frequency = frequency_analysis(guess_list)
        best_score = 0
        if len(suggestions) > 8:            # unless we're down to a few possible solutions,
            for i in guess_list:            # remove words with duplicate letters
                if len(set(i)) < 5:
                    suggestions.remove(i)
        if len(suggestions) == 0:   # if all viable answers contain duplicate letters, the list of suggestions resets
            suggestions = guess_list.copy()
        for i in suggestions:
            score = 0
            if i in answer_list:
                score += 50    # guess words in the answer list are more heavily weighted when fewer guess words remain
            for j in range(5):
                score += letter_frequency[i[j]][j+1]    # this is equivalent to the % frequency with which the letter
            if score > best_score:                      # is in a given position multiplied by the number of times
                best_score = score                      # the letter appears in the word list
                suggestion = i

        print('You should try guessing:', suggestion.upper())
