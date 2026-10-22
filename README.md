# trie_index_utils

A prefix tree (trie) for fast autocomplete over a fixed vocabulary. Provides `TrieIndex` with `contains(word)` for exact membership and `search(prefix)` for prefix-ordered autocompletion.

```python
from trie_index_utils import TrieIndex

t = TrieIndex(["apple", "app", "apply", "apricot", "banana"])
t.contains("app")        # True
t.contains("ap")          # False — prefix only, not a word
t.search("app")           # ["apple", "app", "apply"]
t.search("")              # all words in insertion order
len(t)                    # 5
```

## Why

Autocomplete over a known, fixed word list is a common need, and a trie prunes the search space when a prefix has no continuations. The trade-off here is simplicity: we keep the vocabulary list alongside the trie so results come back in stable insertion order without the nondeterminism of walking trie children via a hash-ordered dict. Memory is O(total characters), which is fine for typical vocabularies of tens of thousands of words.

## Edge cases you'll hit

- **Case sensitivity is on.** `TrieIndex(["Cat"])` will not match `search("c")`. Normalize your vocabulary and queries before construction if you want case-insensitive behavior; the library won't guess your normalization scheme.
- **Empty string is a valid word** if you put it in the vocabulary. `contains("")` reflects that. An empty prefix to `search` returns every word.
- **Duplicates are preserved** in `search` results (insertion order is the source of truth), but `len()` counts unique words. Dedup your input if you don't want duplicates surfacing in suggestions.
- **Non-string vocabulary entries raise `TypeError`** at construction. We don't coerce; coercion hides bugs in the caller's data.
