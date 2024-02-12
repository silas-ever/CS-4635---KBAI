
def is_var(x):
    """
    A helper function that checks if the provided expression x is a variable,
    i.e., a string that starts with ?.

    >>> is_variable('?x')
    True
    >>> is_variable('x')
    False
    """
    return isinstance(x, str) and len(x) > 0 and x[0] == "?"


def substitute(s: dict, x: tuple):
    """
    A helper function that substitute the bindings from s into the expression x.

    >>> substitute({'?x': 'Chris', '?y': 'Dog'}, ('likes', '?x', '?y'))
    ('likes', 'Chris', 'Dog')

    >>> substitute({'?x': 'Dog', '?y': ('owner', '?x')}, ('likes', '?y', '?x'))
    ('likes', ('owner', 'Dog'), 'Dog')

    >>> substitute({'?x': 'Dog'}, '?x')
    'Dog'
    """
    if x in s:
        return substitute(s, s[x])
    elif isinstance(x, tuple):
        return tuple(substitute(s, xi) for xi in x)
    else:
        return x


def unify(x, y, s=None):
    """
    Unify expressions x and y given a provided substitution s. By default s is
    (), which gets recognized and replaced with an empty dictionary. Return a
    substitution (a dict) that will make x and y equal or, if this is not
    possible, then it returns None.

    >>> unify(('likes', '?a', 'B'), ('likes', 'A', 'B'), {})
    {'?a': 'A'}

    >>> unify(('likes', '?a', 'B'), ('likes', 'A', '?b'), {})
    {'?a': 'A', '?b': 'B'}
    """
    if s is None:
        s = {}

    ####### IMPLEMENT THIS FUNCTION #########

    if x == y: # Strings are equal
        return s # No action needed

    elif is_var(x): # Variable?(x)
        return unify_var(x, y, s)
    
    elif is_var(y): # Variable?(y)
        return unify_var(y, x, s)
    
    elif isinstance(x, tuple) and isinstance(y, tuple): # List?(x) and List?(y)
        if len(x) != len(y):
            return None # Edge case
        else:
            for xi, yi in zip(x, y):
                # Get rest of the string for x and y
                x_rest = x[x.index(xi) + 1:]
                y_rest = y[y.index(yi) + 1:]

                # Run unification operation
                s = unify(x_rest, y_rest, unify(x[0], y[0], s))
            
            return s if s != {} else None
        
    else:
        return None # No substitution found


def unify_var(var, x, s):
    """
    Returns a substitution.
    """
    if var in s:
        # {var, val} in s
        return unify(s[var], x, s)
    
    elif x in s:
        # {x, val} in s
        return unify(var, s[x], s) 
    
    elif occurs_check(var, x, s):
        return None  # Failure
    
    else:
        s[var] = x # Save (var, x) to dict
        return s


def occurs_check(var, x, s):
    """
    Function that makes sure a variable does not appear in the element it is 
    bound to, preventing infinite loops.
    """
    if var == x:
        return True
    
    elif is_var(x) and x in s:
        return occurs_check(var, s[x], s) # Recurse
    
    elif isinstance(x, tuple): # Check if x is a list
        return any(occurs_check(var, xi, s) for xi in x)
    
    else:
        return False


def pattern_match(query, kb, substitution=None):
    """
    Similar to unify, but operates over multiple predicates. A query is a list
    of predicates, some of which may contain variables. A knowledge base (kb) is
    a list of predicates without any variables. Substitutions is a dictionary
    mapping variable to values.

    >>> pattern_match([('likes', '?x', 'Dog'), ('has', '?x', 'food')], [('likes', 'Chris', 'Dog'), ('likes', 'Fred', 'Dog'), ('likes', 'Elizabeth', 'Dog'), ('has', 'Chris', 'food'), ('has', 'Elizabeth', 'food')])
    [{'?x': 'Chris'}, {'?x': 'Elizabeth'}]
    """
    if substitution is None:
        substitution = {}
    
    ####### IMPLEMENT THIS FUNCTION #########

    # Recursion base case: no predicates left
    if not query:
        return [substitution]

    result = [] # Initialize result data structure
    q_predicate = query[0] # Retrieve first predicate

    for kb_predicate in kb: # Iterate over KB predicates
        # Create a copy of the existing list
        sub_copy = substitution.copy() 

        # Run unification operation
        unified_sub = unify(q_predicate, kb_predicate, sub_copy)

        if unified_sub is not None: # Unification was successful
            # Index the rest of the query
            q_rest = query[1:]

            # Recursively match remaining predicates
            matches = pattern_match(q_rest, kb, unified_sub)

            if matches: # Matches found
                for match in matches:
                    if match not in result:
                        # Append to result
                        result.extend(matches)

    return result
