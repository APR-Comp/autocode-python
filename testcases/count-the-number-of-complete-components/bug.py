from random import randint
from reference import Solution

from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Grammars import convert_ebnf_grammar
from fuzzingbook.Grammars import Grammar
from fuzzingbook.Grammars import opts 
input_grammar: Grammar = convert_ebnf_grammar({
    "<start>": ["(<integer>,<list>)"],
    "<list>": [("[<pair>(,<pair>)*]",opts(min_depth=20))],
    "<pair>": ["[<integer>,<integer>]"],
    "<integer>": ["<nzdigit><digit>*"],
    "<nzdigit>": [str(x) for x in range(1, 10)],
    "<digit>": [str(x) for x in range(10)]
})

assert is_valid_grammar(input_grammar)


def entrypoint(s: str):
    if s is None:
        return -1

    n, edges = eval(s)
    n = (n % 50) + 1
    edges = list(map(lambda edge: list(map(lambda k: k % n, edge)), edges))
    unique_edge_strings = set(list(map(str, edges)))
    edges = list(map(lambda x: eval(x), unique_edge_strings))

    to_remove = []
    for edge in enumerate(edges):
        if edge[0] == edge[1]:
            to_remove.append(edge)
    for edge in to_remove:
        edges.remove(edge)
    while len(edges) > (n * (n-1)) /2:
        edges.remove(edges[randint(0,len(edges)-1)])
        
    return (n, edges, Solution().countCompleteComponents(n, edges))
