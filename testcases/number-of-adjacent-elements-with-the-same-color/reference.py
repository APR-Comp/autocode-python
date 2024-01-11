from typing import List


class Solution:
    def colorTheArray(self, n: int, queries: List[List[int]]) -> List[int]:
        nums = [0] * n
        answer = []
        adjacent_count = 0
        
        for query in queries:
            index, color = query
            if nums[index] != 0:
                if index > 0 and nums[index] == nums[index - 1]:
                    adjacent_count -= 1
                if index < n - 1 and nums[index] == nums[index + 1]:
                    adjacent_count -= 1
            
            nums[index] = color
            
            if index > 0 and nums[index] == nums[index - 1]:
                adjacent_count += 1
            if index < n - 1 and nums[index] == nums[index + 1]:
                adjacent_count += 1
                
            answer.append(adjacent_count)
        
        return answer
