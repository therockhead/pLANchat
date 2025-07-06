import heapq
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text):
    freq_map = Counter(text)
    heap = [HuffmanNode(c, f) for c, f in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]
  
def build_codes(node, current_code="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is None:
        return code_map
    if node.char is not None:
        code_map[node.char] = current_code
    build_codes(node.left, current_code + "0", code_map)
    build_codes(node.right, current_code + "1", code_map)
    return code_map


def encode(text):
    root = build_tree(text)
    code_map = build_codes(root)
    encoded_text = ''.join(code_map[c] for c in text)
    return encoded_text, code_map

def decode(encoded_text, code_map):
    rev_map = {v: k for k, v in code_map.items()}
    current = ''
    decoded = ''
    for bit in encoded_text:
        current += bit
        if current in rev_map:
            decoded += rev_map[current]
            current = ''
    return decoded
