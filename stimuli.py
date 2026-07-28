import cv2
import time
import numpy as np

class StimuliController:
    def __init__(self):
        self.beep_active = False
        self.flash_active = False

    def beep(self, duration=0.5):
        """Triggers an alert sound."""
        # For Windows, uncomment the line below:
        import winsound
        winsound.Beep(2500, int(duration * 1000))
        
        # Cross-platform bell (works on Mac/Linux/Windows terminal)
        print("\a")
        time.sleep(0.1)

    def flash_screen(self, frame):
        """Overlays a bright white flash."""
        overlay = np.full(frame.shape, 255, dtype=np.uint8)
        flashed_frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        return flashed_frame

    def draw_warning_text(self, frame, level):
        """Draws tiered warning messages."""
        h, w, _ = frame.shape
        
        if level == 1:  # Mild
            cv2.rectangle(frame, (0, 0), (w, h), (0, 255, 255), 15)
            cv2.putText(frame, "⚠️ MILD DROWSINESS", (w//2 - 200, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 4)
            cv2.putText(frame, "Roll down the window!", (w//2 - 150, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        elif level == 2:  # Severe
            cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 255), 20)
            cv2.putText(frame, "🚨 SEVERE DROWSINESS!", (w//2 - 250, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 5)
            cv2.putText(frame, "TURN UP MUSIC! | OPEN WINDOW!", (w//2 - 220, 160), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)
        elif level == 3:  # Emergency
            frame = self.flash_screen(frame)
            cv2.putText(frame, "🛑 PULL OVER NOW 🛑", (w//2 - 300, h//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 8)
            cv2.putText(frame, "VIBRATION ACTIVATED!", (w//2 - 200, h//2 + 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 4)
        return frame