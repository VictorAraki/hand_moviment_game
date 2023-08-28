import cv2
import mediapipe as mp
import numpy as np
import time

class HandTracking:
    def __init__(self):
        self.hand_tracking = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hand_landmarks = None
        self.cap = cv2.VideoCapture(0)
        self.full_list = []

    def _build_frame(self, landmarks):
        np_array = np.zeros((21, 3))
        for i, landmark in enumerate(landmarks):
            np_array[i, 0] = landmark.x
            np_array[i, 1] = landmark.y
            np_array[i, 2] = landmark.z
        return np_array
    

    def save(self):
        np_array = np.array(self.full_list)

        current_time = time.strftime("%Y%m%d_%H%M%S")
        file_name = "data_" + current_time + ".npy"
        np.save(file_name, np_array)
    
    def load(self, path):
        loaded_array = np.load(path)
        return loaded_array

    def scan_hands(self):
        cap_success, self.frame = self.cap.read()
        if cap_success:

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            self.frame = cv2.cvtColor(cv2.flip(self.frame, 1), cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            self.frame.flags.writeable = False

            results = self.hand_tracking.process(self.frame)
            frame_height, frame_width, _ = self.frame.shape

            # Converts image back to BGR
            self.frame.flags.writeable = True
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)

            #default
            m_finger_y = 0
            palm_base_y = 1

            if results.multi_hand_landmarks:
                # For simplicity, we consider only the first hand detected (index 0).
                self.hand_landmarks = results.multi_hand_landmarks[0]

                # # create a list of np_array
                # self.full_list.append(
                #     self._build_frame(
                #         self.hand_landmarks.landmark, 
                #         frame_height, 
                #         frame_width)
                # )
                m_finger_y = self.hand_landmarks.landmark[12].y
                palm_base_y = self.hand_landmarks.landmark[0].y

                # Draw the hand landmarks and connections on the image.
                mp.solutions.drawing_utils.draw_landmarks(
                    self.frame, self.hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style())
                
                # print(f"""
                #       m_finger_y: {m_finger_y}
                #       palm_base_y: {palm_base_y}""")
                
            return m_finger_y, palm_base_y
                

                


    def show_camera(self):
        """Show camera, intended to be used in the game loop
        Args:
            frame: return do cap.read()
        """
        cv2.imshow("Frame", self.frame)
        return cv2.waitKey(5)


    
if __name__ == "__main__":
    hand_tracking = HandTracking()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        hand_tracking.scan_hands()
        key = hand_tracking.show_camera()
        if key == 27: # esc pressed
            break
    cap.release()
    hand_tracking.save()
