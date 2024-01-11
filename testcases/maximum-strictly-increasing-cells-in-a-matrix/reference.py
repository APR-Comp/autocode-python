from typing import List


class Solution:
    def maxIncreasingCells(self, mat: List[List[int]]) -> int:
        m, n = len(mat), len(mat[0])
        r, c = [0] * m, [0] * n
        vmap = {}
        from sortedcontainers import SortedSet
        s = SortedSet()
        for i in range(0, m):
            for j in range(0, n):
                if not -mat[i][j] in vmap:
                    vmap[-mat[i][j]] = []
                vmap[-mat[i][j]].append([i, j])
                s.add(-mat[i][j])
        temp = [[0] * n for _ in range(m)]
        for x in s:
            for v in vmap.get(x):
                temp[v[0]][v[1]] = max(r[v[0]], c[v[1]]) + 1
            for v in vmap.get(x):
                r[v[0]] = max(r[v[0]], temp[v[0]][v[1]])
                c[v[1]] = max(c[v[1]], temp[v[0]][v[1]])
        return max(max(r), max(c))
             