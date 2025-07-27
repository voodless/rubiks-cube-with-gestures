import random
class RubiksCube2x2:
    
    def __init__(self):
        # Each corner: position 0-7
        self.corners_pos = list(range(8))  # [0,1,2,3,4,5,6,7]
        self.corners_ori = [0] * 8         # orientation: 0,1,2
        self.move_history = []
        self.move_stack = []
        self.inverse_moves = {'W': 'S', 'S': 'W', 'A': 'D', 'D': 'A'}

    def pseudo_random_scramble(self,length=20):
        moves = ["W", "A", "S", "D"]
        scramble = []
        prev_move = ''
        for _ in range(length):
            move = random.choice(moves)
            # Avoid consecutive moves on the same face (e.g., U then U')
            while prev_move and move[0] == prev_move[0]:
                move = random.choice(moves)
            scramble.append(move)
            self.apply_move(move)
            prev_move = move
        return scramble
    def apply_move_direct(self, move):
        if move == 'W':
            self._rotate_U(clockwise=True)
        elif move == 'S':
            self._rotate_U(clockwise=False)
        elif move == 'A':
            self._rotate_R(clockwise=True)
        elif move == 'D':
            self._rotate_R(clockwise=False)
        else:
            print("Invalid key")
            return
    def apply_move(self, move):
        if move == 'W':
            self._rotate_U(clockwise=True)
        elif move == 'S':
            self._rotate_U(clockwise=False)
        elif move == 'A':
            self._rotate_R(clockwise=True)
        elif move == 'D':
            self._rotate_R(clockwise=False)
        else:
            print("Invalid key")
            return
    
        self.move_stack.append(move)
        self.move_history.append(move)
    
    def undo_move(self):
        if not self.move_stack:
            print("No moves to undo.")
            return
        last_move = self.move_stack.pop()
        inv_move = self.inverse_moves[last_move]
        self.apply_move_direct(inv_move)
        return last_move

    def _rotate_U(self, clockwise=True):
        # Corners 0,1,2,3 rotate
        if clockwise:
            self.corners_pos[0], self.corners_pos[1], self.corners_pos[2], self.corners_pos[3] = \
                self.corners_pos[1], self.corners_pos[2], self.corners_pos[3], self.corners_pos[0]
        else:
            self.corners_pos[0], self.corners_pos[1], self.corners_pos[2], self.corners_pos[3] = \
                self.corners_pos[3], self.corners_pos[0], self.corners_pos[1], self.corners_pos[2]

    def _rotate_R(self, clockwise=True):
        # Corners 0,3,7,4 rotate
        if clockwise:
            self.corners_pos[0], self.corners_pos[3], self.corners_pos[7], self.corners_pos[4] = \
                self.corners_pos[3], self.corners_pos[7], self.corners_pos[4], self.corners_pos[0]
            # Update orientations: corners on R change twist
            for i in [0,3,7,4]:
                self.corners_ori[i] = (self.corners_ori[i] + 1) % 3
        else:
            self.corners_pos[0], self.corners_pos[3], self.corners_pos[7], self.corners_pos[4] = \
                self.corners_pos[4], self.corners_pos[0], self.corners_pos[3], self.corners_pos[7]
            for i in [0,3,7,4]:
                self.corners_ori[i] = (self.corners_ori[i] - 1) % 3

    def is_solved(self):
        return self.corners_pos == list(range(8)) and all(o == 0 for o in self.corners_ori)
    def reset(self):
        self.corners_pos = list(range(8))
        self.corners_ori = [0] * 8
        self.move_history.clear()
        self.move_stack.clear()
