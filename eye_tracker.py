import cv2
import mediapipe as mp
import numpy as np

class EyeTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # CORRECTED eye indices for MediaPipe
        # These are the standard indices used in many EAR implementations
        self.LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

        # Calibration variables
        self.ear_threshold = 0.25
        self.is_calibrated = False

    def _calculate_ear(self, landmarks, eye_indices):
        """Calculate the Eye Aspect Ratio for given eye landmarks."""
        points = []
        for idx in eye_indices:
            x = landmarks[idx].x
            y = landmarks[idx].y
            points.append([x, y])
        points = np.array(points, dtype=np.float32)

        # EAR formula: (||p1-p5|| + ||p2-p4||) / (2 * ||p0-p3||)
        A = np.linalg.norm(points[1] - points[5])
        B = np.linalg.norm(points[2] - points[4])
        C = np.linalg.norm(points[0] - points[3])

        ear = (A + B) / (2.0 * C)
        return ear

    def calibrate(self, frame):
        """Run this for 3 seconds to find the user's average EAR."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_ear = self._calculate_ear(landmarks, self.LEFT_EYE_INDICES)
            right_ear = self._calculate_ear(landmarks, self.RIGHT_EYE_INDICES)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Set threshold to 70% of the average open-eye value
            self.ear_threshold = avg_ear * 0.7
            self.is_calibrated = True
            print(f"✅ Calibration: Average EAR = {avg_ear:.3f}, Threshold = {self.ear_threshold:.3f}")
            return True
        return False

    def process_frame(self, frame):
        """Processes the frame and returns EAR values."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        left_ear = 0.0
        right_ear = 0.0
        face_detected = False

        if results.multi_face_landmarks:
            face_detected = True
            landmarks = results.multi_face_landmarks[0].landmark

            # Draw the face mesh
            self.mp_drawing.draw_landmarks(
                frame,
                results.multi_face_landmarks[0],
                self.mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles
                .get_default_face_mesh_contours_style()
            )

            left_ear = self._calculate_ear(landmarks, self.LEFT_EYE_INDICES)
            right_ear = self._calculate_ear(landmarks, self.RIGHT_EYE_INDICES)

        return frame, left_ear, right_ear, face_detected