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
        # Initialize variables
        count = 0
        left = 0
        right = 0
        n = len(nums)
        
        # Count the number of good subarray splits
        while right < n:
            if nums[right] == 1:
                # Increase count by the number of elements between left and right (inclusive)
                count += right - left + 1
                
                # Move the left pointer to the next element after the current good subarray split
                left = right + 1
            
            # Move the right pointer to the next element
            right += 1
        
        return count % (10**9 + 7)
