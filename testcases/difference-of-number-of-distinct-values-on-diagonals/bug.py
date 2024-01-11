from reference import Solution
from random import randint
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar
from copy import deepcopy

input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["[<row>(,<row>)+]"],
    "<row>": ["[<integer>(,<integer>)*]"],
    "<integer>": ["<nzdigit><digit>?"],
    "<nzdigit>":[str(x) for x in range(1,10)], 
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)

def entrypoint(s: str):
    if s is None:
        return -1

    l = eval(s)
    
    goal = max(map(len,l))
    if not all( [len(l[i]) == goal for i in range(len(l)) ] ):
        for x in l:
            while len(x) != goal:
                x.append(randint(1,1000))
    
    #print(l)
    #input()

    return (deepcopy(l),Solution().differenceOfDistinctValues(l))
