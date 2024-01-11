from typing import List


class Solution:
    def matrixSum(self, nums: List[List[int]]) -> int:
        score = 0
        while nums:
            highest = 0
            for i in range(len(nums)):
                if nums[i]:
                    num = max(nums[i])
                    nums[i].remove(num)
                    highest = max(highest, num)
            score += highest
            nums = [row for row in nums if row]
        return score
