from cog import BasePredictor, Input, Path
from typing import List
import subprocess
import os
import tempfile

class Predictor(BasePredictor):
    def predict(self,
                video: Path = Input(description="Video to split into frames"),
                fps: int = Input(description="Number of images per second of video, when not exporting all frames", default=1, ge=1),
                extract_all_frames: bool = Input(description="Get every frame of the video. Ignores fps. Slow for large videos.", default=False),
    ) -> List[Path]:
        """Run ffmpeg to split the video into frames"""
        temp_folder_path = tempfile.mkdtemp()

        if not extract_all_frames:
            command = f"ffmpeg -i {video} -vf fps={fps} {temp_folder_path}/out%03d.png"
        else:
            command = f"ffmpeg -i {video} {temp_folder_path}/out%03d.png"

        subprocess.run(command, shell=True, check=True)
        frame_files = sorted(os.listdir(f"{temp_folder_path}"))
        frame_paths = [Path(os.path.join(f"{temp_folder_path}", frame_file)) for frame_file in frame_files]

        return frame_paths
