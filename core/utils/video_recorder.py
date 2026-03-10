import cv2
import numpy as np
import mss
import threading
import time
import os
from datetime import datetime
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager

class VideoRecorder:
    """
    Utility for recording the local screen during test execution.
    
    Uses MSS for fast screen capture and OpenCV for video encoding.
    Recording runs in a background thread to minimize impact on tests.
    """
    def __init__(self, name="test_execution"):
        self.logger = setup_logger(self.__class__.__name__)
        self.name = name
        self.enabled = ConfigManager.get("video.enable_local") or False
        self.fps = ConfigManager.get("video.fps") or 10
        self.recording = False
        self.thread = None
        self.output_path = ""

    def start(self):
        """Starts the recording in a background thread."""
        if not self.enabled or self.recording:
            return

        self.recording = True
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_dir = os.path.abspath("reports/videos")
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
            
        self.output_path = os.path.join(video_dir, f"{self.name}_{timestamp}.mp4")
        self.thread = threading.Thread(target=self._record)
        self.thread.start()
        self.logger.info(f"Video recording started: {self.output_path}")

    def _record(self):
        """Internal recording loop with improved resolution and codec handling."""
        with mss.mss() as sct:
            # Default to index 0 (All monitors) for maximum coverage
            monitor_index = ConfigManager.get("video.monitor_index") or 0
            if monitor_index >= len(sct.monitors):
                monitor_index = 0
            
            monitor = sct.monitors[monitor_index]
            self.logger.info(f"Context: Recording monitor {monitor_index} (logical: {monitor['width']}x{monitor['height']})")
            
            # Capture first frame to get ACTUAL pixel dimensions (handles DPI scaling)
            try:
                first_img = np.array(sct.grab(monitor))
                # Ensure dimensions are even (required by some H.264 encoders)
                height, width = first_img.shape[:2]
                width = (width // 2) * 2
                height = (height // 2) * 2
                self.logger.info(f"Video resolution: {width}x{height} pixels")
            except Exception as e:
                self.logger.error(f"Failed to capture initial frame: {e}")
                return

            # Ensure we use .mp4
            if not self.output_path.endswith(".mp4"):
                self.output_path = os.path.splitext(self.output_path)[0] + ".mp4"

            # Codec Selection (Priority: avc1 > mp4v)
            # avc1 (H.264) is the web standard
            codecs = ['avc1', 'mp4v', 'XVID']
            self.out = None
            
            for code in codecs:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*code)
                    test_out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))
                    if test_out.isOpened():
                        self.out = test_out
                        self.logger.info(f"Initialized VideoWriter with codec: '{code}'")
                        break
                    else:
                        test_out.release()
                        self.logger.warning(f"Codec '{code}' opened but isOpened() returned False.")
                except Exception as e:
                    self.logger.warning(f"Codec '{code}' failed initialization: {e}")

            if not self.out:
                 self.logger.error(f"CRITICAL: Failed to initialize any VideoWriter codec.")
                 return

            frame_count = 0
            total_capture_time = 0
            while self.recording:
                start_time = time.time()
                
                try:
                    # Capture screen
                    sct_img = sct.grab(monitor)
                    img = np.array(sct_img)
                    
                    # Convert to BGR and ensure size matches initialization
                    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                    if frame.shape[1] != width or frame.shape[0] != height:
                        frame = cv2.resize(frame, (width, height))
                    
                    # Write to file
                    self.out.write(frame)
                    frame_count += 1
                except Exception as e:
                    self.logger.error(f"Error capturing frame: {e}")
                    break
                
                capture_duration = time.time() - start_time
                total_capture_time += capture_duration
                
                # Maintain FPS
                sleep_time = (1.0 / self.fps) - capture_duration
                if sleep_time > 0:
                    time.sleep(sleep_time)

            self.out.release()
            avg_fps = frame_count / (total_capture_time + 0.001)
            self.logger.info(f"Recording Finished. Total frames: {frame_count}. Avg Capture Speed: {avg_fps:.2f} FPS")

    def stop(self):
        """Stops the recording thread."""
        if not self.enabled or not self.recording:
            return

        self.recording = False
        if self.thread:
            self.thread.join()
        
        # Calculate real duration using OpenCV
        duration_str = "00:00"
        try:
            cap = cv2.VideoCapture(self.output_path)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                if fps > 0:
                    duration_sec = frame_count / fps
                    mins = int(duration_sec // 60)
                    secs = int(duration_sec % 60)
                    duration_str = f"{mins:02d}:{secs:02d}"
                cap.release()
        except:
            pass

        self.logger.info(f"Video saved: {self.output_path} | Duration: {duration_str}")
