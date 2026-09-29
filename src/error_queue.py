from __future__ import annotations

class ErrorQueue:
    def __init__(self):
        self.items = []
    def push(self, page_idx, reason):
        self.items.append({"page_idx": page_idx, "reason": reason})
    def drain(self):
        out, self.items = self.items, []
        return out
    def depth(self):
        return len(self.items)
