import os
from PIL import Image, ImageChops, ImageDraw
from core.utils.logger_config import setup_logger

class VisualComparer:
    """
    Utility for visual regression testing.
    Compares screenshots against baseline images and generates diffs.
    """
    def __init__(self, baseline_dir="resources/visual/baselines", diff_dir="reports/visual/diffs"):
        self.logger = setup_logger("VisualComparer")
        self.baseline_dir = os.path.abspath(baseline_dir)
        self.diff_dir = os.path.abspath(diff_dir)
        
        # Create directories if they don't exist
        os.makedirs(self.baseline_dir, exist_ok=True)
        os.makedirs(self.diff_dir, exist_ok=True)

    def compare(self, current_image_path: str, test_name: str, threshold: float = 0.01) -> bool:
        """
        Compares the current screenshot with the baseline.
        
        Args:
            current_image_path (str): Path to the recently captured screenshot.
            test_name (str): Unique name for the test (used for baseline filenames).
            threshold (float): Percentage of allowed difference (0.01 = 1%).
            
        Returns:
            bool: True if images match within threshold, False otherwise.
        """
        baseline_path = os.path.join(self.baseline_dir, f"{test_name}.png")
        
        # 1. If no baseline exists, save current as baseline
        if not os.path.exists(baseline_path):
            self.logger.info(f"No baseline found for {test_name}. Saving current image as baseline.")
            Image.open(current_image_path).save(baseline_path)
            return True

        # 2. Open images
        baseline = Image.open(baseline_path).convert("RGB")
        current = Image.open(current_image_path).convert("RGB")

        # 3. Ensure same size
        if baseline.size != current.size:
            self.logger.warning(f"Image size mismatch for {test_name}. Baseline: {baseline.size}, Current: {current.size}")
            # Resize current to match baseline if needed (careful with results)
            current = current.resize(baseline.size)

        # 4. Calculate difference
        diff = ImageChops.difference(baseline, current)
        
        # Calculate percentage of different pixels
        # getbbox returns None if there's no difference
        bbox = diff.getbbox()
        if not bbox:
            self.logger.info(f"Visual match for {test_name} (Identical).")
            return True

        # Count non-zero pixels in the diff image
        cols, rows = diff.size
        # Converting to grayscale and counting pixels > 0
        diff_bw = diff.convert("L")
        num_diff_pixels = sum(1 for pixel in diff_bw.getdata() if pixel > 0)
        total_pixels = cols * rows
        diff_percentage = num_diff_pixels / total_pixels

        self.logger.info(f"Visual diff for {test_name}: {diff_percentage:.2%} (Threshold: {threshold:.2%})")

        if diff_percentage <= threshold:
            self.logger.info("Difference is within threshold.")
            return True

        # 5. Save diff image if failure
        self.logger.error(f"Visual regression failed for {test_name}!")
        diff_output_path = os.path.join(self.diff_dir, f"{test_name}_diff.png")
        
        # Create a red highlighted diff
        mask = diff.convert("L").point(lambda x: 255 if x > 0 else 0)
        highlighted = baseline.copy()
        red_layer = Image.new("RGB", baseline.size, (255, 0, 0))
        highlighted.paste(red_layer, mask=mask)
        
        highlighted.save(diff_output_path)
        self.logger.info(f"Diff image saved to: {diff_output_path}")
        
        return False
