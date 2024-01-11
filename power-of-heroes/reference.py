from typing import *
class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        ans, t, base = 0, 0, 10**9 + 7
        for c in sorted(nums):
            ans = (ans + (t + c) * c * c) % base
            t = (2 * t + c) % base
        return ans