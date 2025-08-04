from cube_state import CubeState

# Available moves for corner-only implementation
MOVE_NAMES = [
    'U', "U'", 'U2',
    'R', "R'", 'R2',
    'F', "F'", 'F2'
]

# Corner permutations and orientations for each move
# Based on standard Rubik's cube corner numbering (0-7)
CORNER_MOVES = {
    # U face moves (top layer rotation)
    "U":   {"perm": [1, 2, 3, 0, 4, 5, 6, 7], "orient": [0]*8},
    "U'":  {"perm": [3, 0, 1, 2, 4, 5, 6, 7], "orient": [0]*8},
    "U2":  {"perm": [2, 3, 0, 1, 4, 5, 6, 7], "orient": [0]*8},
    
    # R face moves (right layer rotation)
    "R":   {"perm": [4, 0, 2, 3, 5, 1, 6, 7], "orient": [1, 1, 0, 0, 1, 1, 0, 0]},
    "R'":  {"perm": [1, 5, 2, 3, 0, 4, 6, 7], "orient": [2, 2, 0, 0, 2, 2, 0, 0]},
    "R2":  {"perm": [5, 4, 2, 3, 1, 0, 6, 7], "orient": [0]*8},
    
    # F face moves (front layer rotation)
    "F":   {"perm": [3, 1, 2, 7, 0, 5, 6, 4], "orient": [1, 0, 0, 1, 1, 0, 0, 1]},
    "F'":  {"perm": [4, 1, 2, 0, 7, 5, 6, 3], "orient": [2, 0, 0, 2, 2, 0, 0, 2]},
    "F2":  {"perm": [7, 1, 2, 4, 3, 5, 6, 0], "orient": [0]*8},
}

class MoveEngine:
    def __init__(self):
        self.moves = {}
        self._define_corner_moves()
    
    def apply_move(self, cube: CubeState, move: str):
        """Apply a move to the cube state"""
        if move in self.moves:
            self.moves[move](cube)
        else:
            raise ValueError(f"Move '{move}' is not defined.")
    
    def define_move(self, name, corner_perm, corner_orient_delta):
        """Define a move with corner permutation and orientation changes"""
        def move_function(cube):
            # Apply permutation to corner positions
            new_positions = [cube.corner_positions[corner_perm[i]] for i in range(8)]
            # Apply orientation changes
            new_orientations = [
                (cube.corner_orientations[corner_perm[i]] + corner_orient_delta[i]) % 3
                for i in range(8)
            ]
            cube.corner_positions = new_positions
            cube.corner_orientations = new_orientations
        
        self.moves[name] = move_function
    
    def _define_corner_moves(self):
        """Initialize all corner moves from the move table"""
        for move_name, move_data in CORNER_MOVES.items():
            self.define_move(move_name, move_data["perm"], move_data["orient"])
    
    def get_available_moves(self):
        """Get list of available moves"""
        return list(self.moves.keys())

# Global move engine instance
engine = MoveEngine()

def apply_move(cube, move):
    """Convenience function to apply a move to a cube"""
    engine.apply_move(cube, move)

def get_inverse_move(move):
    """Get the inverse of a move"""
    if move.endswith("'"):
        return move[:-1]  # R' -> R
    elif move.endswith("2"):
        return move  # R2 -> R2 (self-inverse)
    else:
        return move + "'"  # R -> R'