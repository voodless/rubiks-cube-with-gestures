# Color letters for each face
COLOR_MAP = {
    'U': 'W',  # White
    'D': 'Y',  # Yellow
    'F': 'R',  # Red
    'B': 'O',  # Orange
    'L': 'G',  # Green
    'R': 'B'   # Blue
}

# Each corner maps to 3 face stickers in a fixed order
CORNER_FACELETS = {
    0: ['U', 'R', 'F'],  # URF
    1: ['U', 'F', 'L'],  # UFL
    2: ['U', 'L', 'B'],  # ULB
    3: ['U', 'B', 'R'],  # UBR
    4: ['D', 'F', 'R'],  # DFR
    5: ['D', 'L', 'F'],  # DLF
    6: ['D', 'B', 'L'],  # DBL
    7: ['D', 'R', 'B']   # DRB
}

# Sticker indices on each face for each corner position
FACE_STICKER_INDICES = {
    0: {'U': 0, 'R': 0, 'F': 1},
    1: {'U': 1, 'F': 0, 'L': 1},
    2: {'U': 3, 'L': 0, 'B': 1},
    3: {'U': 2, 'B': 0, 'R': 1},
    4: {'D': 1, 'F': 3, 'R': 2},
    5: {'D': 0, 'L': 3, 'F': 2},
    6: {'D': 2, 'B': 3, 'L': 2},
    7: {'D': 3, 'R': 3, 'B': 2}
}

def get_sticker_colors(cube):
    # Each face now has 8 stickers (2x4)
    faces = {face: [' '] * 8 for face in COLOR_MAP.keys()}

    for pos in range(8):
        cubie = cube.corners_pos[pos]
        ori = cube.corners_ori[pos]

        facelets = CORNER_FACELETS[cubie]
        rotated_facelets = facelets[ori:] + facelets[:ori]

        for face in facelets:
            if face in FACE_STICKER_INDICES[pos]:
                idx = FACE_STICKER_INDICES[pos][face]
                # Map original 4 indices to 8 indices for the big cube
                big_idx = idx * 2
                face_index_in_facelets = facelets.index(face)
                color_face = rotated_facelets[face_index_in_facelets]
                # Fill two adjacent stickers with the same color
                faces[face][big_idx] = COLOR_MAP[color_face]
                faces[face][big_idx + 1] = COLOR_MAP[color_face]

    return faces

class Colors:
    RED = '\033[91m'      # Bright red text
    BLUE = '\033[94m'     # Bright blue text
    GREEN = '\033[92m'    # Bright green text
    YELLOW = '\033[93m'   # Bright yellow text
    WHITE = '\033[97m'    # Bright white text
    ORANGE = '\033[38;5;208m'  # Orange text
    RESET = '\033[0m'     # Reset to normal

COLOR_TO_TERMINAL = {
    'W': Colors.WHITE,   
    'Y': Colors.YELLOW,  
    'R': Colors.RED,     
    'O': Colors.ORANGE,  
    'G': Colors.GREEN,   
    'B': Colors.BLUE     
}

def display_cube(cube):
    faces = get_sticker_colors(cube)
    U, D, F, B, L, R = faces['U'], faces['D'], faces['F'], faces['B'], faces['L'], faces['R']
    
    def c(sticker):
        color = COLOR_TO_TERMINAL.get(sticker, '')
        return f"{color}{sticker}{Colors.RESET}"
    
    print("\nFull Cube Net:\n")

    def face_rows(face):
        return (f"{c(face[4])} {c(face[5])}", f"{c(face[0])} {c(face[1])}")

    u_row1, u_row2 = face_rows(U)
    l_row1, l_row2 = face_rows(L)
    f_row1, f_row2 = face_rows(F)
    r_row1, r_row2 = face_rows(R)
    b_row1, b_row2 = face_rows(B)
    d_row1, d_row2 = face_rows(D)

    # Print top face (U) centered with padding
    print(f"      {u_row1}")
    print(f"      {u_row2}")

    # Print middle row: L F R B faces side by side
    print(f"{l_row1}  {f_row1}  {r_row1}  {b_row1}")
    print(f"{l_row2}  {f_row2}  {r_row2}  {b_row2}")

    # Print bottom face (D) centered
    print(f"      {d_row1}")
    print(f"      {d_row2}")
    
    print("\n3D View:")
    print("        +---------+")
    print(f"       /{c(U[4])} {c(U[5])} / {c(U[6])} {c(U[7])}/|")
    print("       -----+---- |")
    print(f"      /{c(U[0])} {c(U[1])} / {c(U[2])} {c(U[3])}/{c(R[6])}|")
    print(f"     +----+----+ {c(R[5])}|")
    print(f"     |{c(F[0])}  {c(F[1])}|{c(F[2])}  {c(F[3])}|{c(R[0])} |")
    print("     -----+----|/ |")
    print(f"     |{c(F[4])}  {c(F[5])}|{c(F[6])}  {c(F[7])}|{c(R[2])}/")
    print("     +----+----+/")