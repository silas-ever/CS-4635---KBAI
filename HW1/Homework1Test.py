import unittest
from pattern_match import unify
from pattern_match import pattern_match

class Homework1Test(unittest.TestCase):

    #
    # Unify Tests
    #
    def test1(self):
        # Test 1
        # Basic Unify Functionality
        self.assertEqual(unify(('likes', 'Chris', 'dogs'), ('likes', '?y', '?z')), {'?y': 'Chris', '?z': 'dogs'}, "Test 1a Failed")
        self.assertEqual(unify(('likes', 'Chris', 'dogs'), ('likes', 'Chris', '?z')), {'?z': 'dogs'}, "Test 1b Failed")
        self.assertEqual(unify(('likes', 'Chris', 'dogs'), ('likes', '?y', 'dogs')), {'?y': 'Chris'}, "Test 1c Failed")

    def test2(self):
        # Test 2
        # Make sure that unify can also handle standalone variables
        self.assertEqual(unify('John', '?x'), {'?x': 'John'}, "Test 2 Failed")

    def test3(self):
        # Test 3
        # If there are no variables, unify should return an empty array (since no substitutions need to be made)
        self.assertEqual(unify(('likes', 'Chris', 'dogs'), ('likes', 'Chris', 'dogs')), {}, "Test 3a Failed")
        self.assertEqual(unify('John', 'John'), {}, "Test 3b Failed")

    def test4(self):
        # Test 4
        # Return None if there is no way to make x and y equal
        self.assertEqual(unify(('likes', '?x', 'dogs'), ('likes', 'Chris', 'cats')), None, "Test 4a Failed")
        self.assertEqual(unify(('likes', '?x', 'dogs'), ('likes', 'Chris', '?x')), None, "Test 4b Failed")

    def test5(self):
        # Test 5
        # A variable can be equal to a nested tuple
        self.assertEqual(unify(('likes', 'Chris', ('own', 'dogs')), ('likes', 'Chris', '?x')), {'?x': ('own', 'dogs')}, "Test 5 Failed")

    def test6(self):
        # Test 6
        # Make sure to check inside nested tuples for variables as well
        self.assertEqual(unify(('likes', 'Chris', ('own', 'dogs')), ('likes', 'Chris', ('own', '?x'))), {'?x': 'dogs'}, "Test 6 Failed")

    def test7(self):
        # Test 7
        # This one is really weird, but needed to pass all the gradescope test cases. Sometimes the only way to make the test cases equal
        # is to set a variable equal to a nested tuple that contains another variable
        self.assertEqual(unify(('likes', 'Chris', ('own', '?y')), ('likes', 'Chris', '?x')), {'?x': ('own', '?y')}, "Test 7 Failed")

    def test8(self):
        # Test 8
        # Unification of relations (no variables)
        self.assertEqual(unify(('respects', 'Timothy'), ('likes', '?x')), None, "Test 8 Failed")

    def test9(self):
        # Test 9
        # Unification of relations (with variables)
        self.assertEqual(unify(('respects', 'Timothy'), ('likes', '?x')), None, "Test 9a Failed")
        self.assertEqual(unify(('likes', '?x', '?y'), ('respects', 'Dog', 'Pepper')), None, "Test 9b Failed")

    def test10(self):
        # Test 10
        # Unification of nested relations (with variables)
        # 10a: Relations do not match
        self.assertEqual(unify(('on', '?x'), ('off', ('owner', 'Bubby'))), None, "Test 10a Failed")
        # 10b: Different variables and relations cannot map
        self.assertEqual(unify(('likes', '?x', ('friend', '?x')), ('likes', 'Sophia', ('frenemy', 'Summer'))), None, "Test 10b Failed")

    #
    # Pattern Match Tests
    #
    def test11(self):
        # Test 11
        # Basic Pattern Matching Functionality
        a = pattern_match([('likes', '?x', 'dogs')],  [('likes', 'Chris', 'dogs'), ('likes', 'Fred', 'dogs'),  ('likes', 'dogs', ('play', 'fetch')),  ('has', 'Chris', 'food'),  ('like', 'dogs', 'food')])
        b = [{'?x': 'Chris'}, {'?x': 'Fred'}]
        self.assertCountEqual(a, b, "Test 11 Failed")

    def test12(self):
        # Test 12
        # Make sure that the variable satisfies all queries, not just one
        a = pattern_match([('likes', '?x', 'dogs'), ('has', '?x', 'food')],  [('likes', 'Chris', 'dogs'), ('likes', 'Fred', 'dogs'),  ('likes', 'dogs', ('play', 'fetch')),  ('has', 'Chris', 'food'),  ('like', 'dogs', 'food')])
        b = [{'?x': 'Chris'}]
        self.assertCountEqual(a, b, "Test 12 Failed")
        
    def test13(self):
        # Test 13
        # Multiple variables can have the same value in pattern matching
        a = pattern_match([('likes', '?x', 'dogs'), ('likes', '?y', 'dogs')],  [('likes', 'Chris', 'dogs'), ('likes', 'Fred', 'dogs'),  ('likes', 'dogs', ('play', 'fetch')),  ('has', 'Chris', 'food'),  ('like', 'dogs', 'food')])
        b = [{'?x': 'Chris', '?y': 'Fred'}, {'?x': 'Fred', '?y': 'Chris'}, {'?x': 'Chris', '?y': 'Chris'}, {'?x': 'Fred', '?y': 'Fred'}]
        self.assertCountEqual(a, b, "Test 13 Failed")

    def test14(self):
        # Test 14
        # A variable can be equal to a tuple
        a = pattern_match([('likes', 'dogs', '?x')],  [('likes', 'Chris', 'dogs'), ('likes', 'Fred', 'dogs'),  ('likes', 'dogs', ('play', 'fetch')),  ('has', 'Chris', 'food'),  ('likes', 'dogs', 'food')])
        b = [{'?x': ('play', 'fetch')}, {'?x': 'food'}]
        self.assertCountEqual(a, b, "Test 14 Failed")

    def test15(self):
        # Test 15
        # Variables inside tuples should also be accounted for
        a = pattern_match([('likes', '?x', ('play', '?y'))],  [('likes', 'Chris', 'dogs'), ('likes', 'Fred', 'dogs'),  ('likes', 'dogs', ('play', 'fetch')),  ('has', 'Chris', 'food'),  ('like', 'dogs', 'food')])
        b = [{'?x': 'dogs', '?y': 'fetch'}]
        self.assertCountEqual(a, b, "Test 15 Failed")

    def test16(self):
        # Test 16
        # Checks for tuple out of bounds error
        self.assertEqual(unify((), ('a', 'b', 'c')), None, "Test 16 Failed")
    
    def test17(self):
        # Test 17
        # Be sure to return every possible combination of variable-gymnast assignment
        kb = [('gymnast', 'Timmy'), ('gymnast', 'Eric'), ('gymnast', 'Arnold'), ('gymnast', 'Eugene'), ('child', 'Timmy'), ('on', 'Timmy', 'Eric'), ('on', 'Eric', 'Arnold'), ('on', 'Arnold', 'Eugene'), ('on', 'Eugene', 'SpringBoard')]
        query = [('gymnast', '?x'), ('gymnast', '?y'), ('gymnast', '?z'), ('on', '?x', '?y'), ('on', '?y', '?z')]
        
        b = [{'?x': 'Timmy', '?y': 'Eric', '?z': 'Arnold'}, {'?x': 'Eric', '?y': 'Arnold', '?z': 'Eugene'}]
        a = pattern_match(query, kb)
        self.assertEqual(a, b, "Test 17 Failed")

    def test18(self):
        # Test 18
        # There is no requirement for the last variable to be a gymnast
        # Be sure to return every possible combination of variable-gymnast assignment
        kb = [('gymnast', 'Timmy'), ('gymnast', 'Eric'), ('gymnast', 'Arnold'), ('gymnast', 'Eugene'), ('child', 'Timmy'), ('on', 'Timmy', 'Eric'), ('on', 'Eric', 'Arnold'), ('on', 'Arnold', 'Eugene'), ('on', 'Eugene', 'SpringBoard')]
        query = [('gymnast', '?x'), ('gymnast', '?y'), ('on', '?x', '?y'), ('on', '?y', '?z')]
        
        b = [{'?x': 'Timmy', '?y': 'Eric', '?z': 'Arnold'}, {'?x': 'Eric', '?y': 'Arnold', '?z': 'Eugene'}, {'?x': 'Arnold', '?y': 'Eugene', '?z': 'SpringBoard'}]
        a = pattern_match(query, kb)
        self.assertEqual(a, b, "Test 18 Failed")

    def test19(self):
        # Test 19
        # There is no object with relation 'child' that has another object relation 'on' on it
        kb = [('gymnast', 'Timmy'), ('gymnast', 'Eric'), ('gymnast', 'Arnold'), ('gymnast', 'Eugene'), ('child', 'Timmy'), ('on', 'Timmy', 'Eric'), ('on', 'Eric', 'Arnold'), ('on', 'Arnold', 'Eugene'), ('on', 'Eugene', 'SpringBoard')]
        query = [('gymnast', '?x'), ('child', '?y'), ('on', '?x', '?y')]

        b = []
        a = pattern_match(query, kb)
        self.assertEqual(a, b, "Test 19 Failed")

    def test20(self):
        # Test 20
        # Be sure to return every possible combination of variable-gymnast assignment
        kb = [('gymnast', 'Timmy'), ('gymnast', 'Eric'), ('gymnast', 'Arnold'), ('gymnast', 'Eugene'), ('on', 'Timmy', 'Timmy'), ('on', 'Eric', 'Eric'), ('on', 'Timmy', 'Eric')]
        query = [('gymnast', '?x'), ('on', '?x', '?y')]
        
        b = [{'?x': 'Timmy', '?y': 'Timmy'}, {'?x': 'Timmy', '?y': 'Eric'}, {'?x': 'Eric', '?y': 'Eric'}]
        a = pattern_match(query, kb)
        self.assertEqual(a, b, "Test 20 Failed")


if __name__ == "__main__":
    unittest.main()