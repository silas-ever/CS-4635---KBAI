# The autograder has the master branch version of py_search and py_plan
# installed, so you are free to make use of these libraries, or whatever other
# approach you prefer (see https://github.com/cmaclell/py_search and
# https://github.com/cmaclell/py_plan).

def solve_towers_of_hanoi(num_disks: int, source: str, destination: str):
    """
    Solves the towers of hanoi problem in the optimal number of steps.

    num_disks (int) specifies the number of disk, each disk is designated by a
    integer represented as a string; num_disks; this will always be greater
    than 1.

    source (string) specifies the source peg, either "left", "middle", or "right", this
    is the peg that all the disks are initially stacked on.

    destination (string) specifies the destination peg, either "left", "middle", or "right", this
    is the peg that all the disks must end up on to solve the problem.

    The function should return a list of moves, where each move is a tuple with
    three elements: the first element is simply the string "move" representing
    the name of the action (there is only one action here); the second is the
    disk that is being moved, represented as a string (e.g., '1' or '2'); the
    last element is where the disk is being moved to, which is either a peg
    ('left', 'middle', right') or another disk ('1', '2', etc.). 

    >>> solve_towers_of_hanoi(1, 'left', 'left')
    []

    >>> solve_towers_of_hanoi(1, 'left', 'right')
    [('move', '1', 'right')]

    >>> solve_towers_of_hanoi(2, 'left', 'right')
    [('move', '1', 'middle'), ('move', '2', 'right'), ('move', '1', '2')]
   """
    
    # Base cases
    if source == destination: # No move required
        return []
    if num_disks == 0: # Not enough discs to make a move
        return []
    if num_disks == 1: # Only one move needed
        return [('move', '1', destination)]

    # To keep track of what disk is on top of each peg, create stacks
    # Descending order for source peg
    pegs = {source: list(map(str, range(num_disks, 0, -1))), destination: []}

    # Initialize the placeholder peg
    peg_possibilities = ["left", "middle", "right"]
    for peg in peg_possibilities:
        if peg != source and peg != destination:
            pegs[peg] = []

    # Initialize list to keep track of moves taken to solve puzzle
    moves = []
    # print("\nPEGS: ", pegs)
    
    """
    Helper function for a recursive solution the Towers of Hanoi puzzle.

    pegs (dict): keeps track of source and destination stacks
    num_disks (int): number of discs
    source (str): source peg
    placeholder (str): placeholer peg that isn't the source or target
    dest (str): destination peg
    """
    def hanoi_helper(pegs, num_disks, source, placeholder, dest):
        # Base case
        if num_disks == 1:
            move_disk(pegs, source, dest)
        else:
            # Recurse
            hanoi_helper(pegs, num_disks - 1, source, dest, placeholder)
            move_disk(pegs, source, dest)
            hanoi_helper(pegs, num_disks - 1, placeholder, source, dest)
    
    """
    Helper function to move pegs from a source peg to a destination peg.

    pegs (dict): keeps track of source and destination stacks
    from_peg: peg to take a disk from
    to_peg: peg to move disk to
    """
    def move_disk(pegs, from_peg, to_peg):
        # print("\nFROM PEG: ", from_peg)
        # print("\nTO PEG: ", to_peg)
        if from_peg != []: # If source peg is not empty
            disk = pegs[from_peg].pop() # Take a disk off

            if pegs[to_peg] != []: # If destination peg is not empty
                # Move to append should have the disk on the top as the "destination" instead
                moves.append(('move', disk, pegs[to_peg][-1]))
            else: 
                # Move to append should have location as the "destination"
                moves.append(('move', disk, to_peg))
            
            # Add the disk to the destination peg
            pegs[to_peg].append(disk)

    # Call recursive helper function
    hanoi_helper(pegs, num_disks, source, list(set(pegs.keys()) - {source, destination})[0], destination)

    # Return list of moves taken to solve the puzzle
    return moves