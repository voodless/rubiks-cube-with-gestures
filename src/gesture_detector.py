#Vibe coded this ngl
import cv2 as cv
import mediapipe as mp
import sys
import platform
import time
import os
import select

from mediapipe.framework.formats import landmark_pb2 # Still needed for NormalizedLandmarkList

class GestureDetector:
    def __init__(self, gesture_path):
        self.gesture_path = gesture_path
        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.Image = mp.Image
        self.ImageFormat = mp.ImageFormat
        self.RunningMode = mp.tasks.vision.RunningMode

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        self.HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

    def run_cube_game(self, cube, display_cube_func):
        if not os.path.exists(self.gesture_path):
            print(f"ERROR: Gesture recognizer model not found at: {self.gesture_path}")
            print("Please ensure the path is correct and the file exists.")
            return False

        options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path=self.gesture_path),
            running_mode=self.RunningMode.IMAGE
        )

        with self.GestureRecognizer.create_from_options(options) as recognizer:
            cap = None
            camera_found = False
            
            indices_to_try = [0, 1, 2]
            backends_to_try = [cv.CAP_ANY]

            if platform.system() == "Darwin":
                print("Detected macOS. Prioritizing CAP_AVFOUNDATION backend.")
                backends_to_try.insert(0, cv.CAP_AVFOUNDATION)

            for index in indices_to_try:
                for backend in backends_to_try:
                    print(f"Attempting to open camera at index {index} with backend {backend}...")
                    cap = cv.VideoCapture(index, backend)
                    if cap.isOpened():
                        camera_found = True
                        print(f"SUCCESS: Camera opened at index {index} with backend {backend}.")
                        cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
                        cap.set(cv.CAP_PROP_FPS, 30)
                        print(f"  Actual resolution: {cap.get(cv.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv.CAP_PROP_FRAME_HEIGHT)}")
                        print(f"  Actual FPS: {cap.get(cv.CAP_PROP_FPS)}")
                        break
                if camera_found:
                    break

            if not camera_found:
                print("ERROR: Could not open any camera device. Cannot run gesture mode.")
                return False

            print("\n--- Gesture Mode Active ---")
            print("Perform gestures (Pointing Up/Down, Pointing Left/Right) to control the cube. Open palm to exit")
            print("Type 'exit' or 'fail' in terminal, or press 'q' in the camera window to end gesture mode.")
            
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                display_cube_func(cube)

                success, frame = cap.read()
                if not success:
                    print("Failed to read from camera. Ending gesture mode.")
                    break

                frame = cv.flip(frame, 1)
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                mp_image = self.Image(image_format=self.ImageFormat.SRGB, data=rgb_frame)

                detected_gesture_name = None
                move = None

                annotated_frame = frame.copy()

                try:
                    recognition_result = None
                    try:
                        recognition_result = recognizer.recognize(mp_image)
                    except Exception as e:
                        print(f"ERROR DURING GESTURE RECOGNITION (model processing): {e}")
                        recognition_result = None

                    if recognition_result:
                        if recognition_result.hand_landmarks:

                            for current_hand_landmarks_list in recognition_result.hand_landmarks:

                                

                                mp_drawing_proto = landmark_pb2.NormalizedLandmarkList()
                                
                                for lm in current_hand_landmarks_list:
                                    mp_drawing_proto.landmark.add(x=lm.x, y=lm.y, z=lm.z)

                                self.mp_drawing.draw_landmarks(
                                    image=annotated_frame,
                                    landmark_list=mp_drawing_proto,
                                    connections=self.mp_hands.HAND_CONNECTIONS,
                                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                                )
                        
                        if recognition_result.gestures:
                            top_gesture = recognition_result.gestures[0][0]
                            gesture_name_display = top_gesture.category_name
                            score_display = top_gesture.score

                            if top_gesture.score > 0.3:
                                detected_gesture_name = top_gesture.category_name

                                if detected_gesture_name == "Thumb_Up":
                                    move = 'W'
                                    time.sleep(0.45)
                                elif detected_gesture_name == "Thumb_Down":
                                    move = 'S'
                                    time.sleep(0.45)
                                elif detected_gesture_name == "Closed_Fist":
                                    move = 'A'
                                    time.sleep(0.45)
                                elif detected_gesture_name == "Open_Palm":
                                    move = 'D'
                                    time.sleep(0.45)
                                elif detected_gesture_name == "Victory":
                                    move = 'exit'

                            cv.putText(annotated_frame, f'Gesture: {gesture_name_display} ({score_display:.2f})', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                            if move:
                                cv.putText(annotated_frame, f'Move: {move}', (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        else:
                            cv.putText(annotated_frame, 'Gesture: None', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                    cv.imshow('Gesture Recognition (Press Q to exit gesture mode)', annotated_frame)
                    
                    key_pressed = cv.waitKey(1) & 0xFF
                    if key_pressed == ord('q'):
                        print("Exiting gesture mode via 'q' key.")
                        break

                except Exception as e:
                    print(f"ERROR AFTER RECOGNITION (e.g., during drawing/display or game logic): {e}")
                    import traceback
                    traceback.print_exc()
                    break

                if move:
                    print(f"Gesture translated to: {move}")
                else:
                    try:
                        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                            terminal_input = sys.stdin.readline().strip().lower()
                            if terminal_input:
                                move = terminal_input
                                print(f"Terminal input: {move}")
                    except Exception as e:
                        pass

                if move == 'exit':
                    for _ in cube.move_stack:
                        cube.undo_move()
                    print("Exiting application (from gesture mode).")
                    cap.release()
                    cv.destroyAllWindows()
                    sys.exit(0)

                elif move and move.upper() in ['W', 'A', 'S', 'D']:
                    cube.apply_move(move.upper())

                elif move == 'fail':
                    display_cube_func(cube)
                    time.sleep(1)
                    while cube.move_stack:
                        cube.undo_move()
                        sys.stdout.write('\033[8A')
                        sys.stdout.write('\033[2K')
                        os.system('clear' if os.name == 'posix' else 'cls')
                        display_cube_func(cube)
                        sys.stdout.flush()
                        time.sleep(0.2)
                    print("nice try!")
                    cap.release()
                    cv.destroyAllWindows()
                    sys.exit(0)

                elif move:
                    print("Invalid move or command in gesture mode.")
                    time.sleep(0.5)

                if cube.is_solved():
                    print("Cube solved!")
                    break

            cap.release()
            cv.destroyAllWindows()
            return True

    def release(self):
        pass