from collections import deque
from typing import *
class Solution:
    def minCost(self, nums: List[int], x: int) -> int:
        # use dp to memoize seen minimum array
        dp = {} # arr -> min cost
        def cost(maxshift):
            arr = getMinWindow(maxshift + 1)
            key = tuple(arr)
            if key in dp:
                dp[key] = min(dp[key], maxshift * x + sum(arr))
            else:
                dp[key] = maxshift * x + sum(arr)
            return dp[key]
            
        # see sliding window maximum problem, leetcode hard
        def getMinWindow(k):
            res = []
            minq = deque()
            m = len(nums)
            lst = nums + nums.copy()
            for i, n in enumerate(lst):
                if i >= k and minq and minq[0] == lst[i - k]:
                    minq.popleft()
                while minq and n < minq[-1]:
                    minq.pop()
                minq.append(n)
                if i >= k - 1:
                    res.append(minq[0])
                if i == m + k - 2:
                    break
            return res[:m]
                
        # binary search to look for the right shift
        lo, hi = 0, len(nums) - 1

        while lo < hi:
            mid = (lo + hi) // 2
            if cost(mid) <= cost(mid + 1):
                hi = mid
            else:
                lo = mid + 1
            
        return cost(lo)