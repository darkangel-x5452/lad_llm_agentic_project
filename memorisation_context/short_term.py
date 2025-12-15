class ShortTermMemory:
    def __init__(self, max_len=10):
        self.buffer = []
        self.max_len = max_len

    def add(self, role, content):
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.max_len:
            self.buffer.pop(0)

    def get_context(self):
        return "\n".join(f"{m['role']}: {m['content']}" for m in self.buffer)
