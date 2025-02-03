import sys
from pathlib import Path

# project file path
ROOT = Path(__file__).resolve().parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
ROOT = ROOT.relative_to(Path.cwd())
ASSET_DIR = ROOT / 'assets'

# model path
MODEL_PATH = ROOT / 'model'
LINE_MODEL_PATH = MODEL_PATH / 'line_test_best100.pt'
HELMET_MODEL_PATH = MODEL_PATH / 'helm_test_best50.pt'
CROSSWALK_MODEL_PATH = MODEL_PATH / 'yolov5_crosswalk_best50.pt'

# input source
STATIC = 'Static'
UPLOAD = 'Upload'
LINK = 'Link'
WEBCAM = 'Webcam'
SOURCE_LIST = [STATIC, UPLOAD, LINK, WEBCAM]

# static videos
STATIC_VIDEOS_DIR = ASSET_DIR / 'videos'
VIDEOS_DICT = {
    'Line video': STATIC_VIDEOS_DIR / 'video_line.mp4',
    'Helmet video': STATIC_VIDEOS_DIR / 'video_helm.mp4',
}

# webcam (0 default 1 obs)
# index based on computer webcam index
WEBCAM_PATH = 1

# const text
INPUT_VIDEO = 'Input video'
OUTPUT_VIDEO = 'Output video'