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
        if not self.enabled:
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
        """Internal recording loop."""
        with mss.mss() as sct:
            # Default to index 0 (All monitors) for maximum coverage
            monitor_index = ConfigManager.get("video.monitor_index") or 0
            if monitor_index >= len(sct.monitors):
                monitor_index = 0
            
            monitor = sct.monitors[monitor_index]
            self.logger.info(f"Recording monitor {monitor_index} (All Displays): {monitor}")

            # Use MJPG codec - very high compatibility, albeit larger files
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            width = int(monitor["width"])
            height = int(monitor["height"])
            
            # Use .avi for MJPG
            if self.output_path.endswith(".mp4"):
                self.output_path = self.output_path.replace(".mp4", ".avi")

            out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))

            frame_count = 0
            total_capture_time = 0
            while self.recording:
                start_time = time.time()
                
                try:
                    # Capture screen
                    sct_img = sct.grab(monitor)
                    img = np.array(sct_img)
                    
                    # MJPG/OpenCV expects BGR (mss gives BGRA)
                    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                    
                    # Write to file
                    out.write(frame)
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

            out.release()
            avg_fps = frame_count / (total_capture_time + 0.001)
            self.logger.info(f"Recording Finished. Total frames: {frame_count}. Avg Capture Speed: {avg_fps:.2f} FPS")

    def stop(self):
        """Stops the recording thread."""
        if not self.enabled or not self.recording:
            return

        self.recording = False
        if self.thread:
            self.thread.join()
        self.logger.info(f"Video recording stopped and saved to: {self.output_path}")
