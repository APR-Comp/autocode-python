from typing import *
"""python
 You are given a binary array nums.
A subarray of an array is good if it contains exactly one element with the value 1.
Return an integer denoting the number of ways to split the array nums into good subarrays. As the number may be too large, return it modulo 109 + 7.
A subarray is a contiguous non-empty sequence of elements within an array.
 
Example 1:

Input: nums = [0,1,0,0,1]
Output: 3
Explanation: There are 3 ways to split nums into good subarrays:
- [0,1] [0,0,1]
- [0,1,0] [0,1]
- [0,1,0,0] [1]

Example 2:

Input: nums = [0,1,0]
Output: 1
Explanation: There is 1 way to split nums into good subarrays:
- [0,1,0]

 
Constraints:

1 <= nums.length <= 105
0 <= nums[i] <= 1

 """
class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        suffix = [0] * (n + 2)
        mod = 10**9 + 7
        ans = 0
        
        # Calculating prefix array
        for i in range(1, n + 1):
            prefix[i] = prefix[i - 1] + nums[i - 1]
        
        # Calculating suffix array
        for i in range(n, 0, -1):
            suffix[i] = suffix[i + 1] + nums[i - 1]
        
        # Counting good subarray splits
        for i in range(1, n + 1):
            if nums[i - 1] == 1:
                ans = (ans + prefix[i - 1]) % mod
                ans = (ans + suffix[i + 1]) % mod
        
        return ans
