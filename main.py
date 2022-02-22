
ANSWERS = "wordle-answers-alphabetical.txt"     # https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
GUESSES = "wordle-allowed-guesses.txt"          # https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c


# TODO: work on duplicate letters
def filter_words(wor, pat, word_list):
    c = ['_', '_', '_', '_', '_']
    u = ['_', '_', '_', '_', '_']
    deconfirmed = ""

    for i in range(5):
        if pat[i] == 'g':
            c[i] = wor[i]
        if pat[i] == 'y':
            u[i] = wor[i]
        if pat[i] == 'b':
            if wor[i] not in c and wor[i] not in u:
                deconfirmed += wor[i]

    confirmed = "".join(c)
    unconfirmed = "".join(u)

    i = 0
    while i < len(word_list):
        for j in range(5):
            if confirmed[j] != '_' and word_list[i][j] != confirmed[j]:
                word_list.remove(word_list[i])
                i -= 1
                break
        else:
            for j in unconfirmed:
                if j != '_':
                    if j not in word_list[i]:
                        word_list.remove(word_list[i])
                        i -= 1
                        break
                    else:
                        for j in range(5):
                            if word_list[i][j] == unconfirmed[j]:
                                word_list.remove(word_list[i])
                                i -= 1
                                break
            else:
                for j in deconfirmed:
                    if j in word_list[i]:
                        word_list.remove(word_list[i])
                        i -= 1
                        break
        i += 1


def frequency_analysis(al):
    lf = {}         # letter frequency

    for i in range(0, 26):
        lf[chr(97 + i)] = [0, 0, 0, 0, 0, 0]

    counter = 1     # counter keeps track of the letter's position in the word
    for i in al:    # answer list
        for j in i:
            if j != '\n':
                lf[j][0] += 1
                lf[j][counter] += 1
                counter += 1
            else:
                counter = 1

    return lf


if __name__ == '__main__':
    obj = open(ANSWERS)
    answer_list = obj.readlines()
    obj.close()

    obj = open(GUESSES)
    guess_list = obj.readlines()
    obj.close()

    letter_frequency = frequency_analysis(answer_list)
    viable_answers = answer_list.copy()
    viable_guesses = guess_list.copy()
    temp = []
    suggestions = []
    suggestion = ''

    print('Welcome to Wordle Helper!')
    while True:
        print(len(viable_answers))
        word = input('What was your guess?\n').lower()
        print()
        if word == 'qqqqq':
            viable_answers = answer_list.copy()
            viable_guesses = guess_list.copy()
            print('Restarting')
            continue
        pattern = input('What was the color pattern? For example, if the first letter was green, the second was yellow,'
                        ' and the other three were black, you would type GYBBB:\n').lower()
        print()

        # filter answers that are no longer viable
        filter_words(word, pattern, viable_answers)
        suggestions = viable_answers.copy()
        letter_frequency = frequency_analysis(viable_answers)
        for i in letter_frequency.keys():
            if letter_frequency[i][0] == 0:
                temp.append(i)
        for i in temp:
            del letter_frequency[i]
        temp = sorted(letter_frequency, key=letter_frequency.get, reverse=True)
        temp.clear()

        best_score = 0
        if len(suggestions) > 8:
            for i in suggestions:       # remove words with duplicate letters
                if len(set(i)) < 6:
                    temp.append(i)
            for i in temp:
                suggestions.remove(i)

        if len(suggestions) == 0:   # if all viable answers contain duplicate letters, the list of suggestions resets
            suggestions = viable_answers.copy()

        for i in suggestions:
            score = 0
            for j in range(5):
                score += letter_frequency[i[j]][0]
            if score > best_score:
                best_score = score
                suggestion = i
        temp.clear()

        print('You should try guessing:', suggestion.upper())
