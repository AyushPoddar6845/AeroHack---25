class CubeState:
    def __init__(self):
        # 8 corners: position (which corner is where) and orientation (0,1,2)
        self.corner_positions = list(range(8))
        self.corner_orientations = [0] * 8
        # 12 edges: position and orientation (0,1) - kept for future expansion
        self.edge_positions = list(range(12))
        self.edge_orientations = [0] * 12
    
    def copy(self):
        """Create a deep copy of the cube state"""
        new_cube = CubeState()
        new_cube.corner_positions = self.corner_positions[:]
        new_cube.corner_orientations = self.corner_orientations[:]
        new_cube.edge_positions = self.edge_positions[:]
        new_cube.edge_orientations = self.edge_orientations[:]
        return new_cube
    
    def is_solved(self):
        """Check if cube is in solved state"""
        return (self.corner_positions == list(range(8)) and
                self.corner_orientations == [0] * 8 and
                self.edge_positions == list(range(12)) and
                self.edge_orientations == [0] * 12)
    
    def __eq__(self, other):
        """Equality comparison for cube states"""
        if not isinstance(other, CubeState):
            return False
        return (self.corner_positions == other.corner_positions and
                self.corner_orientations == other.corner_orientations and
                self.edge_positions == other.edge_positions and
                self.edge_orientations == other.edge_orientations)
    
    def __hash__(self):
        """Hash function for use in sets and dictionaries"""
        return hash((tuple(self.corner_positions), tuple(self.corner_orientations),
                    tuple(self.edge_positions), tuple(self.edge_orientations)))
    
    def get_corner_key(self):
        """Get corner state as tuple for pattern database lookup"""
        return tuple(self.corner_positions + self.corner_orientations)