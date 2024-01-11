from typing import *

class Solution:
    def minimizedStringLength(self, s: str) -> int:
        return len(set((s)))