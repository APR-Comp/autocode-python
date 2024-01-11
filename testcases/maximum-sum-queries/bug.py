from reference import Solution
from random import randint
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar

input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["(<row>,<row>,[<query> (,<query>)+ ] )"],
    "<row>": ["[<integer>(,<integer>)+]"],
    "<query>": ["[<integer>,<integer>]"],
    "<integer>": ["<nzdigit><digit>?"],
    "<nzdigit>":[str(x) for x in range(1,10)], 
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)

def entrypoint(s: str):
    if s is None:
        return -1

    n_one,n_two,queries = eval(s)
    
    while len(n_one) > len(n_two):
        n_two.append(randint(1,1e9))
    
    while len(n_two) > len(n_one):
        n_one.append(randint(1,1e9))
    
    
    #print(n_one,n_two,queries)
    #input()

    return (n_one,n_two,queries,Solution().maximumSumQueries(n_one,n_two,queries))
