import fuzzingbook
from fuzzingbook import GreyboxFuzzer as gbf
from fuzzingbook import Coverage as cv
from fuzzingbook import MutationFuzzer as mf
from fuzzingbook import GrammarCoverageFuzzer as gcf

from typing import List, Set, Any, Tuple, Dict, Union

import os
import traceback
import numpy as np
import time

from bug import entrypoint
from bug import input_grammar

# You can re-implement the coverage class to change how
# the fuzzer tracks new behavior in the SUT


class MyCoverage(cv.Coverage):
    def coverage(self) -> Set[cv.Location]:
        """The set of executed lines, as (function_name, line_number) pairs"""
        # print(self.trace())
        return self.trace()


# You can re-implement the runner class to change how
# the fuzzer tracks new behavior in the SUT

class MyFunctionCoverageRunner(mf.FunctionRunner):
    def run_function(self, inp: str) -> Any:
        with MyCoverage() as cov:
            try:
                result = super().run_function(inp)
            except Exception as exc:
                print(exc)
                input()
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        return (inp, self._coverage, result)

    def coverage(self) -> Set[cv.Location]:
        return self._coverage


# class MyRunner(mf.FunctionRunner):
#
#     def run_function(self, inp):
#           <your implementation here>
#
#     def coverage(self):
#           <your implementation here>
#
#     etc...


# You can re-implement the fuzzer class to change your
# fuzzer's overall structure

# class MyFuzzer(gbf.GreyboxFuzzer):
#
#     def reset(self):
#           <your implementation here>
#
#     def run(self, runner: gbf.FunctionCoverageRunner):
#           <your implementation here>
#   etc...

# The Mutator and Schedule classes can also be extended or
# replaced by you to create your own fuzzer!


# When executed, this program should run your fuzzer for a very
# large number of iterations. The benchmarking framework will cut
# off the run after a maximum amount of time
#
# The `get_initial_corpus` and `entrypoint` functions will be provided
# by the benchmarking framework in a file called `bug.py` for each
# benchmarking run. The framework will track whether or not the bug was
# found by your fuzzer -- no need to keep track of crashing inputs
template = """
import solution

def test_{id}():
	assert solution.Solution().{funcname}({args}) == {res}
"""
import importlib
if __name__ == "__main__":
    fast_schedule = gbf.AFLFastSchedule(5)
    line_runner = MyFunctionCoverageRunner(entrypoint)

    fuzzer = gcf.GrammarCoverageFuzzer(input_grammar)
    testcases = fuzzer.runs(line_runner, trials=100000)
    #testcases.sort(key=lambda x: len(x[0][1]))
    #covered_places = set()

    # for ((string, coverage, processed_data), outcome) in testcases:
    #     if processed_data == -1:
    #         continue
    #     # new_covered = False
    #     # for i,loc in enumerate(coverage[1:]):
    #     #     edge = (coverage[i],loc)
    #     #     if edge not in covered_places:
    #     #         new_covered = True
    #     #         covered_places.add(edge)
    #     # if not new_covered:
    #     #     continue
    #     if str(coverage) in covered_places:
    #         continue
    #     covered_places.add(str(coverage))
    #     *processed_input, output = processed_data
    #     print(processed_input)
    #     # print("()")

    os.makedirs('outputs', exist_ok=True)
    
    import reference
    
    public_methods = list(filter(lambda x :not x.startswith('__'),dir(reference.Solution)))
    
    if len(public_methods) != 1:
        print("More than one public method. This is not okay")
        input()
    
    funcname =public_methods[0]
    
    for i, ((string, coverage, processed_data), outcome) in enumerate(testcases):
        *processed_input, output = processed_data
        with open('outputs/newtest_{}.py'.format(i),'w') as f:
            f.write(template.format(id=i, funcname=funcname,
                    args=','.join(map(str,processed_input)), res=output))
