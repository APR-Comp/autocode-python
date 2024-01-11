import random
from reference import Solution

from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar

input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["<integer>"],
    "<integer>": ["<nzdigit><digit>?"],
    "<nzdigit>": [str(x) for x in range(1, 10)],
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)


def entrypoint(s: str):
    if s is None:
        return -1

    x = eval(s)
    
    x = max(1,x % 50) + 1
    
    l = list(range(1,x+1))
    random.shuffle(l)
    
    #print(x,l)
    #input()

    return (l, Solution().semiOrderedPermutation(l))
