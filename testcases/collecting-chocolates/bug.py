from reference import Solution

from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar,opts
input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": [("(<integer>,[<integer>(,<integer>)*])",opts(min_depth=10) )],
    "<integer>": ["<nzdigit><digit>*"],
    "<nzdigit>":[str(x) for x in range(1,10)], 
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)

def entrypoint(s: str):
    if s is None:
        return -1

    x, l = eval(s)
    return (l,x, Solution().minCost(l,x))
