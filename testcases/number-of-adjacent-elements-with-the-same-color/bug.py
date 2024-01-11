from reference import Solution
from random import randint
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar

input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["(<integer>, [<row>(,<row>)+])"],
    "<row>": ["[<integer>,<integer>]"],
    "<integer>": ["<nzdigit><digit>?"],
    "<nzdigit>":[str(x) for x in range(1,10)], 
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)

def entrypoint(s: str):
    if s is None:
        return -1

    n,l = eval(s)
    l = list(map(lambda x : (x[0] % n, x[1]),l))
    
    #print(l)
    #input()

    return (n,l,Solution().colorTheArray(n,l))
