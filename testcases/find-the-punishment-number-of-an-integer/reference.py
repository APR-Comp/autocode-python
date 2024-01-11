class Solution:
    def punishmentNumber(self, n: int) -> int:
        def is_punishment_num(num : int) -> bool:
            square = num * num
            str_square = str(square)
            length = len(str_square)
            for i in range(1 << length):
                split = []
                last = 0
                for j in range(length):
                    if ((i >> j) & 1) == 1:
                        split.append(int(str_square[last:j+1]))
                        last = j+1
                if last != length:
                    split.append(int(str_square[last:length]))
                if sum(split) == num:
                    return True
            return False

        punishment_number = 0
        for i in range(1, n + 1):
            if is_punishment_num(i):
                punishment_number += i * i
        return punishment_number
