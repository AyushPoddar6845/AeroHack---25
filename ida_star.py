def ida_star_search(start, goal_check_fn, heuristic_fn, move_set, apply_move_fn, max_depth=20):
    """
    Iterative Deepening A* search for optimal Rubik's cube solving.
    
    Args:
        start: Initial cube state
        goal_check_fn: Function to check if goal is reached
        heuristic_fn: Admissible heuristic function
        move_set: Available moves
        apply_move_fn: Function to apply moves to cube state
        max_depth: Maximum search depth
    
    Returns:
        List of moves to solve cube, or None if no solution found
    """
    # Initialize threshold with heuristic estimate
    threshold = heuristic_fn(start)
    
    # Early exit if already solved
    if goal_check_fn(start):
        return []
    
    nodes_explored = 0
    
    def dfs(node, g, threshold, path, last_move=None):
        """
        Depth-first search with f-cost threshold and move pruning.
        
        Args:
            node: Current cube state
            g: Current path cost (depth)
            threshold: Current f-cost threshold
            path: Current move sequence
            last_move: Last move applied (for pruning)
        
        Returns:
            - List of moves if solution found
            - Minimum f-cost if threshold exceeded
            - float('inf') if no valid moves
        """
        nonlocal nodes_explored
        nodes_explored += 1
        
        # Calculate f-cost (g + h)
        h = heuristic_fn(node)
        f = g + h
        
        # Threshold cutoff
        if f > threshold:
            return f
        
        # Goal check
        if goal_check_fn(node):
            return path
        
        # Depth limit safety
        if g >= max_depth:
            return float('inf')
        
        min_cost = float('inf')
        
        # Try all moves with basic pruning
        for move in move_set:
            # Avoid immediate reversal (basic pruning)
            if last_move and are_opposite_moves(move, last_move):
                continue
            
            # Apply move to copy of current state
            next_node = node.copy()
            apply_move_fn(next_node, move)
            
            # Recursive search
            result = dfs(next_node, g + 1, threshold, path + [move], move)
            
            # Solution found
            if isinstance(result, list):
                return result
            
            # Update minimum cost for next iteration
            if result < min_cost:
                min_cost = result
        
        return min_cost
    
    # Iterative deepening loop
    iteration = 0
    while threshold <= max_depth:
        iteration += 1
        nodes_explored = 0
        
        print(f"IDA* iteration {iteration}: threshold = {threshold}")
        
        result = dfs(start, 0, threshold, [])
        
        # Solution found
        if isinstance(result, list):
            print(f"Solution found in {iteration} iterations, explored {nodes_explored} nodes")
            return result
        
        # No solution possible
        if result == float('inf'):
            break
        
        # Update threshold for next iteration
        threshold = result
        print(f"  Explored {nodes_explored} nodes, new threshold = {threshold}")
    
    print(f"No solution found within depth {max_depth}")
    return None

def are_opposite_moves(move1, move2):
    """
    Check if two moves are opposites (cancel each other out).
    This provides basic move pruning to avoid inefficient sequences.
    
    Args:
        move1, move2: Move strings (e.g., 'R', "R'", 'R2')
    
    Returns:
        True if moves are opposites
    """
    if not move1 or not move2:
        return False
    
    # Get base face (remove ' and 2 suffixes)
    face1 = move1[0]
    face2 = move2[0]
    
    # Must be same face
    if face1 != face2:
        return False
    
    # Define opposite relationships
    opposites = {
        ('', "'"),   # R and R'
        ("'", ''),   # R' and R
        ('2', '2'),  # R2 and R2 (self-inverse)
    }
    
    suffix1 = move1[1:] if len(move1) > 1 else ''
    suffix2 = move2[1:] if len(move2) > 1 else ''
    
    return (suffix1, suffix2) in opposites

def print_search_stats(nodes_explored, iterations, solution_length):
    """Print search statistics for analysis"""
    print(f"\n📊 Search Statistics:")
    print(f"   Nodes explored: {nodes_explored:,}")
    print(f"   IDA* iterations: {iterations}")
    print(f"   Solution length: {solution_length} moves")
    print(f"   Nodes per move: {nodes_explored // max(1, solution_length):,}")