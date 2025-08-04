import os
import pickle
from collections import deque
from cube_state import CubeState
from move_engine import apply_move, MOVE_NAMES

# Database file for caching
DB_FILE = "corner_db_fast.pkl"

def generate_corner_pattern_database(max_depth=7, force_regenerate=False):
    """
    Generate corner pattern database using BFS from solved state.
    This creates an admissible heuristic for IDA* search.
    
    Args:
        max_depth: Maximum depth to explore (7 is good balance of size/quality)
        force_regenerate: Force regeneration even if cache exists
    
    Returns:
        Dictionary mapping corner states to minimum move counts
    """
    # Check if cached database exists
    if not force_regenerate and os.path.exists(DB_FILE):
        print(f"Loading cached pattern database from {DB_FILE}")
        try:
            with open(DB_FILE, "rb") as f:
                db = pickle.load(f)
                print(f"Loaded {len(db)} corner pattern entries")
                return db
        except (pickle.PickleError, FileNotFoundError, EOFError):
            print("Cache corrupted, regenerating...")
    
    print(f"Generating corner pattern database (max depth: {max_depth})...")
    
    # BFS from solved state
    solved_cube = CubeState()
    queue = deque([(solved_cube, 0)])
    visited = set()
    db = {}
    
    states_processed = 0
    
    while queue:
        current_state, depth = queue.popleft()
        
        # Get corner state key
        corner_key = current_state.get_corner_key()
        
        # Skip if already visited or too deep
        if corner_key in visited or depth > max_depth:
            continue
        
        # Mark as visited and add to database
        visited.add(corner_key)
        db[corner_key] = depth
        states_processed += 1
        
        # Progress reporting
        if states_processed % 50000 == 0:
            print(f"Processed {states_processed} states at depth {depth}")
        
        # Generate successor states
        for move in MOVE_NAMES:
            next_state = current_state.copy()
            apply_move(next_state, move)
            
            next_key = next_state.get_corner_key()
            if next_key not in visited:
                queue.append((next_state, depth + 1))
    
    print(f"Pattern database generation complete: {len(db)} entries")
    
    # Cache the database
    try:
        with open(DB_FILE, "wb") as f:
            pickle.dump(db, f)
        print(f"Database cached to {DB_FILE}")
    except Exception as e:
        print(f"Warning: Could not save database cache: {e}")
    
    return db

def corner_heuristic(cube_state, pattern_db):
    """
    Heuristic function that returns minimum moves to solve corners.
    This is admissible (never overestimates) for IDA*.
    
    Args:
        cube_state: Current cube state
        pattern_db: Precomputed pattern database
    
    Returns:
        Minimum number of moves to solve corners (lower bound)
    """
    corner_key = cube_state.get_corner_key()
    return pattern_db.get(corner_key, float('inf'))

def validate_pattern_database(pattern_db):
    """Validate that the pattern database is correct"""
    solved_cube = CubeState()
    solved_key = solved_cube.get_corner_key()
    
    if solved_key not in pattern_db:
        raise ValueError("Pattern database missing solved state!")
    
    if pattern_db[solved_key] != 0:
        raise ValueError(f"Solved state should have distance 0, got {pattern_db[solved_key]}")
    
    print("Pattern database validation passed")
    return True