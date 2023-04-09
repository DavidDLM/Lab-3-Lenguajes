import re
from machine import *
from postfix import *
from thompson import Thompson


class TokenCompiler:
    def __init__(this, filename):
        this.filename = filename

    def compileTokens(this, output_file):
        automatas = []
        joinTokens = []
        individualNFA = []
        token_nfa_map = {}
        counter = -1
        fileTokens = Tokens()
        fileTokens.tokenize(this.filename)

        # Combine tokens that are substrings of other tokens
        for i in range(len(fileTokens.tokens)):
            for j in range(len(fileTokens.tokens)):
                if i != j and fileTokens.tokens[i][0] in fileTokens.tokens[j][1]:
                    fileTokens.tokens[i] = (
                        fileTokens.tokens[i][0], fileTokens.tokens[i][1], True)
                    break
                else:
                    fileTokens.tokens[i] = (
                        fileTokens.tokens[i][0], fileTokens.tokens[i][1], False)

        # Generate individual NFAs for each token
        for token in fileTokens.tokens:
            if token[2]:
                postfix = shunting_yard(token[1])
                # print(postfix)
                tokenNFA = Thompson(regex=postfix, counter=counter)
                tokenNFA.compile()
                counter = tokenNFA.counter
                automatas.append((token, tokenNFA))
                token_nfa_map[token[0]] = tokenNFA

        # Join tokens with regular expressions
        # Use joinTokens = []
        for token in fileTokens.tokens:
            if token[2]:
                joinTokens.append(token[1])
            else:
                operators = []
                regex_splitted = re.findall('\w+|[+*?()|.]', token[1])
                operators.extend(regex_splitted)

                for i, element in enumerate(operators):
                    '''
                    if element in token_nfa_map:
                        operators[i] = "("+token_nfa_map[element].regex+")"
                    new_regex = ''.join(operators)

                    join_tokens.append(new_regex)

                    '''
                    for tokenNFA in automatas:
                        if element == tokenNFA[0][0]:
                            operators[i] = "("+tokenNFA[0][1]+")"
                new_regex = ''.join(operators)

                joinTokens.append((token[0], new_regex, token[2]))

        # Generate NFAs for joined tokens
        for token in joinTokens:
            if not token[2]:
                postfix = shunting_yard(token[1])
                # print(postfix)
                tokenNFA = Thompson(regex=postfix, counter=counter)
                tokenNFA.compile()
                counter = tokenNFA.counter
                automatas.append((token, tokenNFA))

        # NFA list
        individualNFA = [tokenNFA for _,
                         tokenNFA in automatas if tokenNFA is not None]

        finalNFA = Thompson(counter=counter, automatas=individualNFA)
        finalNFA.lex_automata(output_file)
