from reference import Solution
from random import randint
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar

input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["[<row>(,<row>)+]"],
    "<row>": ["[<integer>(,<integer>)*]"],
    "<integer>": ["0", "1"],
})

assert is_valid_grammar(input_grammar)


def entrypoint(s: str):
    if s is None:
        return -1

    l = eval(s)

    goal = max(map(len, l))
    if not all([len(l[i]) == goal for i in range(len(l))]):
        for x in l:
            while len(x) != goal:
                x.append(randint(0,1))

    #print(l)
    #input()

    return (l, Solution().goodSubsetofBinaryMatrix(l))
