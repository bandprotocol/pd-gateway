from pdgateway.cache import LRUCache, LinkedNode
import unittest

from typing import List

class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.lru_cache = LRUCache(3)

    def test_is_hit_empty(self):
        is_hit = self.lru_cache.is_hit("test")
        self.assertFalse(is_hit)
    
    def test_is_hit(self):
        self.lru_cache.put("key1", "test1")
        self.assertTrue(self.lru_cache.is_hit("key1"))
        self.assertFalse(self.lru_cache.is_hit("key2"))

        self.lru_cache.put("key2", "test2")
        self.assertTrue(self.lru_cache.is_hit("key1"))
        self.assertTrue(self.lru_cache.is_hit("key2"))
        self.assertFalse(self.lru_cache.is_hit("key3"))
    
    def test_unlimited_cache(self):
        self.lru_cache = LRUCache(0)
        self.lru_cache.put("key1", "test1")
        self.lru_cache.put("key2", "test2")
        self.assertEqual("test1", self.lru_cache.d["key1"].val)
        self.assertEqual("test2", self.lru_cache.d["key2"].val)

        self.assertEqual(self.lru_cache.d["key2"].prev, None)
        self.assertEqual(self.lru_cache.d["key2"].next, self.lru_cache.d["key1"])
        self.assertEqual(self.lru_cache.d["key1"].prev, self.lru_cache.d["key2"])
        self.assertEqual(self.lru_cache.d["key1"].next, None)
        
    
    def test_limited_cache(self):
        self.lru_cache.put("key1", "test1")
        self.lru_cache.put("key2", "test2")
        self.lru_cache.put("key3", "test3")
        self.lru_cache.put("key4", "test4")

        self.assertEqual(self.lru_cache.d["key4"].prev, None)
        self.assertEqual(self.lru_cache.d["key4"].next, self.lru_cache.d["key3"])
        self.assertEqual(self.lru_cache.d["key3"].prev, self.lru_cache.d["key4"])
        self.assertEqual(self.lru_cache.d["key3"].next, self.lru_cache.d["key2"])
        self.assertEqual(self.lru_cache.d["key2"].prev, self.lru_cache.d["key3"])
        self.assertEqual(self.lru_cache.d["key2"].next, None)
    
    def test_reuse_cache(self):
        self.lru_cache.put("key1", "test1")
        self.lru_cache.put("key2", "test2")
        self.lru_cache.put("key3", "test3")
        self.lru_cache.put("key2", "test4")
        self.assertTrue(self.lru_cache.is_hit("key1"))
        self.assertTrue(self.lru_cache.is_hit("key2"))
        self.assertTrue(self.lru_cache.is_hit("key3"))
        self.assertEqual("key2", self.lru_cache.d["key2"].key)
        self.assertEqual("key3", self.lru_cache.d["key3"].key)
        self.assertEqual("key1", self.lru_cache.d["key1"].key)
        self.assertEqual("test4", self.lru_cache.d["key2"].val)
        self.assertEqual("test3", self.lru_cache.d["key3"].val)
        self.assertEqual("test1", self.lru_cache.d["key1"].val)


        self.assertEqual(self.lru_cache.head, self.lru_cache.d["key2"])
        self.assertEqual(self.lru_cache.tail, self.lru_cache.d["key1"])
        self.assertEqual(self.lru_cache.d["key2"].prev, None)
        self.assertEqual(self.lru_cache.d["key2"].next, self.lru_cache.d["key3"])
        self.assertEqual(self.lru_cache.d["key3"].prev, self.lru_cache.d["key2"])
        self.assertEqual(self.lru_cache.d["key3"].next, self.lru_cache.d["key1"])
        self.assertEqual(self.lru_cache.d["key1"].prev, self.lru_cache.d["key3"])
        self.assertEqual(self.lru_cache.d["key1"].next, None)

        self.lru_cache.put("key4", "test44")
        self.lru_cache.put("key5", "test55")
        self.lru_cache.put("key2", "test5")
        self.assertFalse(self.lru_cache.is_hit("key1"))
        self.assertTrue(self.lru_cache.is_hit("key2"))
        self.assertFalse(self.lru_cache.is_hit("key3"))
        self.assertTrue(self.lru_cache.is_hit("key4"))
        self.assertTrue(self.lru_cache.is_hit("key5"))

        self.assertEqual(self.lru_cache.head, self.lru_cache.d["key2"])
        self.assertEqual(self.lru_cache.tail, self.lru_cache.d["key4"])
        self.assertEqual(self.lru_cache.d["key2"].prev, None)
        self.assertEqual(self.lru_cache.d["key2"].next, self.lru_cache.d["key5"])
        self.assertEqual(self.lru_cache.d["key5"].prev, self.lru_cache.d["key2"])
        self.assertEqual(self.lru_cache.d["key5"].next, self.lru_cache.d["key4"])
        self.assertEqual(self.lru_cache.d["key4"].prev, self.lru_cache.d["key5"])
        self.assertEqual(self.lru_cache.d["key4"].next, None)
    
    def test_reuse_cache_2(self):
        self.lru_cache.put("key1", "test1")
        self.lru_cache.put("key1", "test1")
        self.assertTrue(self.lru_cache.is_hit("key1"))
        self.assertEqual("key1", self.lru_cache.d["key1"].key)
        self.assertEqual("test1", self.lru_cache.d["key1"].val)
        self.assertEqual(self.lru_cache.head, self.lru_cache.d["key1"])
        self.assertEqual(self.lru_cache.tail, self.lru_cache.d["key1"])
        self.assertEqual(self.lru_cache.d["key1"].prev, None)
        self.assertEqual(self.lru_cache.d["key1"].next, None)




