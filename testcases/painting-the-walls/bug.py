from reference import Solution
from random import randint
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar


input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["(<list>,<list>)"],
    "<list>": ["[<integer>(,<integer>)*]"],
    "<integer>": ["<nzdigit><digit>*"],
    "<nzdigit>": [str(x) for x in range(1, 10)],
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)

def entrypoint(s: str):
    if s is None:
        return -1

    cost,time = eval(s)
    time = list(map(lambda x : x % 500, time))
    
    while len(cost)> len(time):
        time.append(randint(1,500))
    
    while len(time) > len(cost):
        cost.append(randint(1,10000))
    
    #print(cost,time)
    #input()

    return (cost,time,Solution().paintWalls(cost,time))
