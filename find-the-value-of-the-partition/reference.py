from typing import *
class Solution:
    def findValueOfPartition(self, nums: List[int]) -> int:
                # Sort the given array
        nums.sort()
        
        # Initialize the minimum partition value to be the maximum integer
        min_partition = float('inf')
        
        # Loop through the array from the second element to the last
        for i in range(1, len(nums)):
            
            # Calculate the absolute difference between the current element and the previous one
            partition = abs(nums[i] - nums[i-1])
            
            # If this partition value is smaller than the current minimum, update the minimum
            if partition < min_partition:
                min_partition = partition
                
        return min_partition
