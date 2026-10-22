import unittest

from trie_index_utils import TrieIndex


class TestTrieIndexConstruction(unittest.TestCase):
    def test_empty_vocabulary_yields_empty_index(self):
        t = TrieIndex([])
        self.assertEqual(len(t), 0)
        self.assertEqual(t.search(""), [])
        self.assertFalse(t.contains(""))

    def test_non_string_entry_raises_type_error(self):
        with self.assertRaises(TypeError):
            TrieIndex(["ok", 42])


class TestTrieIndexContains(unittest.TestCase):
    def test_exact_match_present(self):
        t = TrieIndex(["cat", "car", "card"])
        self.assertTrue(t.contains("cat"))
        self.assertTrue(t.contains("car"))
        self.assertTrue(t.contains("card"))

    def test_prefix_only_not_treated_as_word(self):
        t = TrieIndex(["card"])
        self.assertFalse(t.contains("car"))
        self.assertFalse(t.contains("ca"))
        self.assertFalse(t.contains("c"))

    def test_non_string_contains_returns_false(self):
        t = TrieIndex(["cat"])
        self.assertFalse(t.contains(None))
        self.assertFalse(t.contains(42))

    def test_empty_string_not_a_word(self):
        t = TrieIndex(["a", ""])
        self.assertTrue(t.contains(""))


class TestTrieIndexSearch(unittest.TestCase):
    def test_prefix_returns_matches(self):
        words = ["cat", "car", "card", "dog"]
        t = TrieIndex(words)
        result = t.search("ca")
        self.assertEqual(result, ["cat", "car", "card"])

    def test_full_word_prefix_returns_that_word(self):
        t = TrieIndex(["cat", "car"])
        self.assertEqual(t.search("cat"), ["cat"])

    def test_empty_prefix_returns_all_in_order(self):
        words = ["dog", "cat", "car"]
        t = TrieIndex(words)
        self.assertEqual(t.search(""), words)

    def test_no_match_returns_empty_list(self):
        t = TrieIndex(["cat", "car"])
        self.assertEqual(t.search("z"), [])
        self.assertEqual(t.search("cats"), [])

    def test_non_string_prefix_raises(self):
        t = TrieIndex(["cat"])
        with self.assertRaises(TypeError):
            t.search(42)

    def test_case_sensitive(self):
        t = TrieIndex(["Cat", "cat"])
        self.assertEqual(t.search("C"), ["Cat"])
        self.assertEqual(t.search("c"), ["cat"])
        self.assertEqual(t.search("cat"), ["cat"])
        self.assertTrue(t.contains("Cat"))
        self.assertTrue(t.contains("cat"))

    def test_duplicates_preserved_in_search(self):
        t = TrieIndex(["cat", "cat", "car"])
        self.assertEqual(t.search("ca"), ["cat", "cat", "car"])
        self.assertEqual(len(t), 2)


class TestTrieIndexLen(unittest.TestCase):
    def test_size_counts_unique_words(self):
        t = TrieIndex(["a", "a", "b"])
        self.assertEqual(len(t), 2)


class TestTrieIndexInOperator(unittest.TestCase):
    def test_in_operator_matches_contains(self):
        t = TrieIndex(["cat"])
        self.assertIn("cat", t)
        self.assertNotIn("car", t)


if __name__ == "__main__":
    unittest.main()
