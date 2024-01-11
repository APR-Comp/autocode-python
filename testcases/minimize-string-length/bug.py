from reference import Solution
from random import randint
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar

input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["\"<letter>+\""],
    "<letter>": list(map(chr,range(ord('a'),ord('z')+1)))
})

assert is_valid_grammar(input_grammar)

def entrypoint(s: str):
    if s is None:
        return -1

    l = eval(s)
    
    #print(l)
    #input()

    return ('"'+l+'"',Solution().minimizedStringLength(l))
