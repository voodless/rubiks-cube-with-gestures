import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from cube_logic import RubiksCube2x2
from cube_renderer import display_cube
import time
import sys
from gesture_detector import GestureDetector as gd

cube = RubiksCube2x2()
cube.pseudo_random_scramble(15)

gesture_path = '/Users/elie080106/Downloads/rubiks-cube-master/src/assets/gesture_recognizer.task'
detector = gd(gesture_path) 

try:
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_cube(cube)
        
        print("\n--- Input Mode Selection ---")
        print("1. WASD (Keyboard Control)")
        print("2. Gestures (Camera Control)")
        print("3. Exit")
        
        choice = input("Select input mode: ").lower()

        if choice == '1':
            print("\n--- WASD Mode Active ---")
            while True: 
                os.system('clear' if os.name == 'posix' else 'cls')
                display_cube(cube)
                
                move = input("Enter move (WASD), 'fail', 'exit', or 'm' for mode select: ").lower()

                if move == 'exit':
                    for _ in cube.move_stack:
                        cube.undo_move()
                    print("Exiting application (from WASD mode).")
                    sys.exit(0)

                elif move == 'm': 
                    print("Returning to mode selection.")
                    time.sleep(1)
                    break # Break inner WASD loop to go back to outer mode select loop

                elif move.upper() in ['W', 'A', 'S', 'D']:
                    cube.apply_move(move.upper())

                elif move == 'fail':
                    display_cube(cube)
                    time.sleep(1)
                    while cube.move_stack:
                        cube.undo_move()
                        sys.stdout.write('\033[8A')
                        sys.stdout.write('\033[2K')
                        os.system('clear' if os.name == 'posix' else 'cls')
                        display_cube(cube)
                        sys.stdout.flush()
                        time.sleep(0.2)
                    print("nice try!")
                    sys.exit(0) 

                else:
                    print("Invalid move")
                    time.sleep(0.5)

                if cube.is_solved():
                    print("Cube solved!")
                    time.sleep(2) 
                    sys.exit(0) 

        elif choice == '2':
            # Call the gesture detector's run_cube_game method
            print("Attempting to start gesture mode...")
            success = detector.run_cube_game(cube, display_cube)
            if not success:
                print("Gesture mode could not be started. Returning to mode selection.")
                time.sleep(2) # Allow user to read message


        elif choice == '3':
            print("Exiting application.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            time.sleep(1) # Give time to read message

finally:

    pass 