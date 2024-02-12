import unittest
from towers_of_hanoi import solve_towers_of_hanoi

class Homework2Test(unittest.TestCase):
    def test_OneTowerNoMoves(self):
        self.assertEqual(solve_towers_of_hanoi(1, 'left', 'left'), [])
        self.assertEqual(solve_towers_of_hanoi(1, 'middle', 'middle'), [])
        self.assertEqual(solve_towers_of_hanoi(1, 'right', 'right'), [])

    def test_OneTowerOneMoveRight(self):
        self.assertEqual(solve_towers_of_hanoi(1, 'left', 'right'), [('move', '1', 'right')])
        self.assertEqual(solve_towers_of_hanoi(1, 'middle', 'right'), [('move', '1', 'right')])

    def test_OneTowerOneMoveMiddle(self):
        self.assertEqual(solve_towers_of_hanoi(1, 'left', 'middle'), [('move', '1', 'middle')])
        self.assertEqual(solve_towers_of_hanoi(1, 'right', 'middle'), [('move', '1', 'middle')])

    def test_OneTowerOneMoveLeft(self):
        self.assertEqual(solve_towers_of_hanoi(1, 'middle', 'left'), [('move', '1', 'left')])
        self.assertEqual(solve_towers_of_hanoi(1, 'right', 'left'), [('move', '1', 'left')])

    def test_two_disks_left_to_right(self):
        result = solve_towers_of_hanoi(2, 'left', 'right')
        expected = [
            ('move', '1', 'middle'), 
            ('move', '2', 'right'), 
            ('move', '1', '2')
        ]
        self.assertEqual(result, expected)

    def test_two_disks_no_moves(self):
        result = solve_towers_of_hanoi(2, 'left', 'left')
        expected = []
        self.assertEqual(result, expected)

    def test_test_two_disks_middle_to_right(self):
        result = solve_towers_of_hanoi(2, 'middle', 'right')
        expected = [
            ('move', '1', 'left'),
            ('move', '2', 'right'),
            ('move', '1', '2')
        ]
        self.assertEqual(result, expected)

    def test_test_three_disks(self):
        result = solve_towers_of_hanoi(3, 'left', 'right')
        expected = [
            ('move', '1', 'right'),
            ('move', '2', 'middle'),
            ('move', '1', '2'),
            ('move', '3', 'right'),
            ('move', '1', 'left'),
            ('move', '2', '3'),
            ('move', '1', '2')
        ]
        self.assertEqual(result, expected)

    def test_four_disks(self):
        print('four disks')
        result = solve_towers_of_hanoi(4, 'left', 'right')
        expected = [
            ('move', '1', 'middle'), 
            ('move', '2', 'right'), 
            ('move', '1', '2'), 
            ('move', '3', 'middle'), 
            ('move', '1', '4'), 
            ('move', '2', '3'), 
            ('move', '1', '2'), 
            ('move', '4', 'right'), 
            ('move', '1', '4'), 
            ('move', '2', 'left'), 
            ('move', '1', '2'), 
            ('move', '3', '4'), 
            ('move', '1', 'middle'), 
            ('move', '2', '3'), 
            ('move', '1', '2')
        ]
        self.assertEqual(result, expected)