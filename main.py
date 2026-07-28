import cv2
import time
import csv
from datetime import datetime
from eye_tracker import EyeTracker
from stimuli import StimuliController

def main():
    print("=" * 50)
    print("🧠 NEURODRIVE - Drowsiness Reversal via Stimuli")
    print("=" * 50)

    # Initialize our classes
    tracker = EyeTracker()
    stimuli = StimuliController()
    
    # Start Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Error: Could not open camera. Please check your webcam.")
        return

    # CALIBRATION PHASE (3 seconds)
    print("\n📷 Calibrating... Please look straight at the camera for 3 seconds.")
    start_calib = time.time()
    calibrated = False
    
    while time.time() - start_calib < 3.0:
        ret, frame = cap.read()
        if not ret:
            continue
        if tracker.calibrate(frame):
            calibrated = True
            break
        cv2.putText(frame, f"Calibrating... {int(3.0 - (time.time() - start_calib))}s", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("NeuroDrive Setup", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    if not calibrated:
        print("⚠️ Warning: No face detected. Using default threshold.")
    else:
        print("✅ Calibration complete! Starting monitoring...")

    # Variables for Drowsiness Detection
    drowsy_start_time = None
    current_alert_level = 0
    total_blinks = 0
    
    # CSV Logging
    log_file = open("drowsiness_log.csv", "w", newline="")
    log_writer = csv.writer(log_file)
    log_writer.writerow(["Timestamp", "Drowsy_Duration (sec)", "Max_Level_Reached"])

    print("\n🟢 System Running! Press 'q' to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera disconnected. Trying to reconnect...")
            cap.release()
            cap = cv2.VideoCapture(0)
            time.sleep(1)
            continue

        # Process frame and get EAR
        processed_frame, left_ear, right_ear, face_detected = tracker.process_frame(frame)
        avg_ear = (left_ear + right_ear) / 2.0

        # Display EAR on screen
        cv2.putText(processed_frame, f"EAR: {avg_ear:.3f} (Threshold: {tracker.ear_threshold:.3f})", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(processed_frame, f"Blinks: {total_blinks}", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # ---------- DROWSINESS LOGIC ----------
        if avg_ear < tracker.ear_threshold and face_detected:
            # Eyes are CLOSED
            if drowsy_start_time is None:
                drowsy_start_time = time.time()
                current_alert_level = 0
            else:
                elapsed = time.time() - drowsy_start_time
                
                # TIERED ALERTS
                if elapsed > 5.0 and current_alert_level < 3:
                    current_alert_level = 3
                    stimuli.beep(1.0)
                    processed_frame = stimuli.draw_warning_text(processed_frame, 3)
                    print("🚨 EMERGENCY! Pull over!")
                    
                elif elapsed > 3.0 and current_alert_level < 2:
                    current_alert_level = 2
                    stimuli.beep(0.5)
                    processed_frame = stimuli.draw_warning_text(processed_frame, 2)
                    print("⚠️ SEVERE Drowsiness detected!")
                    
                elif elapsed > 1.5 and current_alert_level < 1:
                    current_alert_level = 1
                    stimuli.beep(0.2)
                    processed_frame = stimuli.draw_warning_text(processed_frame, 1)
                    print("⚠️ Mild Drowsiness detected...")
                else:
                    if current_alert_level > 0:
                        processed_frame = stimuli.draw_warning_text(processed_frame, current_alert_level)
        else:
            # Eyes are OPEN
            if drowsy_start_time is not None:
                closed_duration = time.time() - drowsy_start_time
                if closed_duration < 0.4:  # Normal blink
                    total_blinks += 1
                else:
                    # Drowsy episode ended - log it
                    log_writer.writerow([datetime.now(), f"{closed_duration:.2f}", current_alert_level])
                    log_file.flush()
                    print(f"📝 Logged episode: {closed_duration:.2f} seconds")
                
                drowsy_start_time = None
                current_alert_level = 0

        # Show the frame
        cv2.imshow("NeuroDrive - Drowsiness Reversal", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    log_file.close()
    print("\n🛑 Shutdown complete. Log saved to drowsiness_log.csv")

if __name__ == "__main__":
    main()