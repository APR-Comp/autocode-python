
import solution

def test_3861():
	assert solution.Solution().maximumSumQueries([1, 7],[4, 8],[[5, 8], [6, 7], [9, 1], [1, 8]]) == [15, 15, -1, 15]
