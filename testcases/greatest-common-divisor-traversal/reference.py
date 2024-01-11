import math
from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        MAX = max(nums)+1
        primes = [i for i in range(MAX)]
        for i in range(2, int(math.sqrt(MAX))+1):
            if primes[i] == i:
                for j in range(i*i, MAX, i):
                    primes[j] = min(i, primes[j])

        graph = [[] for _ in range(n)]
        last_prime_index = [-1]*MAX
        for i in range(n):
            x = nums[i]
            while x > 1:
                prime = primes[x]
                if last_prime_index[prime] != -1:
                    graph[i].append(last_prime_index[prime])
                    graph[last_prime_index[prime]].append(i)
                last_prime_index[prime] = i
                while x % prime == 0:
                    x //= prime

        seen = [0]*n
        def dfs(i):
            seen[i] = 1
            for j in graph[i]:
                if not seen[j]:
                    dfs(j)

        dfs(0)
        return all(seen)
