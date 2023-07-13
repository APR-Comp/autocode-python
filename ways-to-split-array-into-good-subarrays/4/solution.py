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
        left = [0] * n
        right = [0] * n
        left_cnt = 0
        right_cnt = 0
        ans = 0

        # Calculate the count of 1's from left side
        for i in range(n):
            if nums[i] == 1:
                left_cnt += 1
            left[i] = left_cnt

        # Calculate the count of 1's from right side
        for i in range(n-1, -1, -1):
            if nums[i] == 1:
                right_cnt += 1
            right[i] = right_cnt

        # Count the number of good subarray splits
        for i in range(n-1):
            if left[i] > 0 and right[i+1] > 0:
                ans += min(left[i], right[i+1])

        return ans % (10**9 + 7)
