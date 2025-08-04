import random
import time
import sys
from cube_state import CubeState
from move_engine import apply_move, MOVE_NAMES
from pattern_db import generate_corner_pattern_database, corner_heuristic, validate_pattern_database
from ida_star import ida_star_search

# Increase recursion limit for deep searches
sys.setrecursionlimit(15000)

def generate_scramble(length=8):
    """Generate a random scramble sequence"""
    return [random.choice(MOVE_NAMES) for _ in range(length)]

def apply_scramble(cube, scramble):
    """Apply scramble moves to cube"""
    for move in scramble:
        apply_move(cube, move)
    return cube

def verify_solution(scramble, solution):
    """Verify that the solution actually solves the scrambled cube"""
    # Apply scramble
    test_cube = CubeState()
    apply_scramble(test_cube, scramble)
    
    # Apply solution
    for move in solution:
        apply_move(test_cube, move)
    
    return test_cube.is_solved()

def main():
    print("🧩 Rubik's Cube Solver - Kociemba Two-Phase Algorithm Demo")
    print("=" * 60)
    
    # Step 1: Generate scramble
    scramble = generate_scramble(length=8)  # Keep short for demo
    print(f"🎲 Generated scramble: {scramble}")
    
    # Step 2: Create scrambled cube
    cube = CubeState()
    apply_scramble(cube, scramble)
    
    if cube.is_solved():
        print("⚠️  Warning: Generated scramble results in solved cube (rare but possible)")
        return
    
    # Step 3: Load/generate pattern database
    print("\n📊 Loading pattern database...")
    db_start_time = time.time()
    corner_db = generate_corner_pattern_database(max_depth=7)
    db_end_time = time.time()
    
    print(f"📦 Pattern DB entries: {len(corner_db):,}")
    print(f"⏱️  DB load/generation time: {db_end_time - db_start_time:.2f} seconds")
    
    # Validate database
    try:
        validate_pattern_database(corner_db)
    except ValueError as e:
        print(f"❌ Database validation failed: {e}")
        return
    
    # Step 4: Define heuristic function
    def heuristic_fn(cube_state):
        return corner_heuristic(cube_state, corner_db)
    
    # Check initial heuristic estimate
    initial_heuristic = heuristic_fn(cube)
    print(f"🎯 Initial heuristic estimate: {initial_heuristic} moves")
    
    # Step 5: Solve using IDA*
    print(f"\n🔍 Starting IDA* search...")
    solve_start_time = time.time()
    
    solution = ida_star_search(
        start=cube,
        goal_check_fn=lambda c: c.is_solved(),
        heuristic_fn=heuristic_fn,
        move_set=MOVE_NAMES,
        apply_move_fn=apply_move,
        max_depth=15  # Reasonable limit for corner-only solving
    )
    
    solve_end_time = time.time()
    
    # Step 6: Display results
    print("\n" + "=" * 60)
    if solution:
        print("✅ Solution found!")
        print(f"🎯 Scramble: {scramble}")
        print(f"🔧 Solution: {solution}")
        print(f"🔢 Move count: {len(solution)} moves")
        print(f"⏱️  Solve time: {solve_end_time - solve_start_time:.3f} seconds")
        
        # Verify solution
        if verify_solution(scramble, solution):
            print("✅ Solution verified: Cube is solved!")
        else:
            print("❌ Solution verification failed!")
    else:
        print("❌ No solution found within depth limit")
        print("💡 Try increasing max_depth or check cube state")
    
    # Performance summary
    total_time = solve_end_time - db_start_time
    print(f"\n📈 Total runtime: {total_time:.3f} seconds")
    
    if solution:
        print(f"🏆 Average time per move: {(solve_end_time - solve_start_time) / len(solution):.4f} seconds")

def demo_with_specific_scramble():
    """Demo function with a known scramble for testing"""
    print("🧪 Running demo with specific scramble...")
    
    # Known scramble that should be solvable
    test_scramble = ['R', 'U', 'F']
    print(f"Test scramble: {test_scramble}")
    
    cube = CubeState()
    apply_scramble(cube, test_scramble)
    
    corner_db = generate_corner_pattern_database(max_depth=7)
    
    solution = ida_star_search(
        start=cube,
        goal_check_fn=lambda c: c.is_solved(),
        heuristic_fn=lambda c: corner_heuristic(c, corner_db),
        move_set=MOVE_NAMES,
        apply_move_fn=apply_move,
        max_depth=10
    )
    
    if solution:
        print(f"Solution: {solution}")
        if verify_solution(test_scramble, solution):
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")
    else:
        print("❌ No solution found for test scramble")

if __name__ == "__main__":
    try:
        main()
        # Uncomment for additional testing:
        # print("\n" + "="*60)
        # demo_with_specific_scramble()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback
        traceback.print_exc()