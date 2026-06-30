"""
WINDOWS SETUP GUIDE FOR FISH PIPELINE
A complete step-by-step guide to set up and run the fish detection pipeline on Windows 10/11.
"""

# ============================================================================
# STEP 1: INSTALL PYTHON
# ============================================================================

# Option A: Direct from Python.org (Recommended)
# 1. Download Python 3.10+ from https://www.python.org/downloads/
# 2. Run the installer
# 3. ✅ CHECK: "Add Python to PATH" (important!)
# 4. Click "Install Now"
# 5. Verify installation:
#    - Open Command Prompt (Win+R, type "cmd", Enter)
#    - Type: python --version
#    - Should show: Python 3.10.x or higher

# Option B: Using Windows Package Manager (if you have it)
# winget install Python.Python.3.11

# ============================================================================
# STEP 2: INSTALL VS CODE
# ============================================================================

# 1. Download from https://code.visualstudio.com/
# 2. Run installer, accept defaults
# 3. Launch VS Code
# 4. Open Extensions (Ctrl+Shift+X)
# 5. Install these extensions:
#    - Python (by Microsoft)
#    - Pylance
#    - Git Graph (optional, for version control)
#    - YAML (for config file syntax highlighting)

# ============================================================================
# STEP 3: DOWNLOAD THE PROJECT
# ============================================================================

# Option A: Using Git (recommended)
# 1. Download Git from https://git-scm.com/download/win
# 2. Run installer with defaults
# 3. Open Command Prompt and run:
#    cd C:\Users\YourUsername\Desktop
#    git clone https://github.com/beingmyself6002/fish-pipeline.git
#    cd fish-pipeline

# Option B: Manual download
# 1. Go to https://github.com/beingmyself6002/fish-pipeline
# 2. Click "Code" → "Download ZIP"
# 3. Extract to: C:\Users\YourUsername\Desktop\fish-pipeline

# ============================================================================
# STEP 4: OPEN IN VS CODE
# ============================================================================

# 1. In VS Code: File → Open Folder
# 2. Navigate to C:\Users\YourUsername\Desktop\fish-pipeline
# 3. Click "Select Folder"
# 4. Trust the workspace if prompted

# ============================================================================
# STEP 5: CREATE VIRTUAL ENVIRONMENT IN VS CODE
# ============================================================================

# 1. Press Ctrl+` (backtick) to open Terminal in VS Code
# 2. Run the following commands:

# For Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get an error about execution policy:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again: .\venv\Scripts\Activate.ps1

# For Windows (Command Prompt):
python -m venv venv
venv\Scripts\activate.bat

# ✅ Your terminal should now show (venv) at the start of the prompt line

# ============================================================================
# STEP 6: SELECT PYTHON INTERPRETER IN VS CODE
# ============================================================================

# 1. Press Ctrl+Shift+P (Command Palette)
# 2. Type: Python: Select Interpreter
# 3. Choose the one that says "./venv/bin/python" or similar
# 4. Confirm it shows "(venv)" in the terminal

# ============================================================================
# STEP 7: INSTALL DEPENDENCIES
# ============================================================================

# With the terminal still open and (venv) active, run:
pip install --upgrade pip
pip install -r requirements.txt

# This will take 5-10 minutes (downloading ~1-2 GB of packages)
# Wait for it to complete - don't close the terminal

# ✅ When done, you should see: "Successfully installed [X] packages"

# ============================================================================
# STEP 8: VERIFY INSTALLATION
# ============================================================================

# 1. In VS Code terminal (with venv active), run:
python -c "import cv2, torch, ultralytics; print('✓ All imports successful!')"

# If successful, you'll see: ✓ All imports successful!
# If not, there's an installation issue - see Troubleshooting below

# ============================================================================
# STEP 9: SET UP PROJECT FOLDERS
# ============================================================================

# The folder structure should already exist, but verify:
# In VS Code, expand the folder tree on the left (Explorer view)
# You should see:
# - data/
#   - raw_frames/
#   - enhanced_frames/
#   - labels/
#   - classes.yaml
# - src/
#   - enhance.py
#   - prepare_dataset.py
#   - train_detector.py
#   - train_classifier.py
#   - infer_pipeline.py
#   - utils.py
# - models/
# - outputs/
# - config.yaml
# - requirements.txt

# If any folders are missing, create them:
# Right-click in Explorer → New Folder

# ============================================================================
# STEP 10: PREPARE YOUR DATA
# ============================================================================

# 1. Place raw underwater frames in: data/raw_frames/
#    (e.g., frame_001.jpg, frame_002.jpg, ...)

# 2. To enhance frames, open terminal in VS Code and run:
python src/enhance.py --input data/raw_frames --output data/enhanced_frames

# ============================================================================
# STEP 11: RUN ENHANCEMENT (STAGE 1)
# ============================================================================

# Terminal command:
python src/enhance.py --input data/raw_frames --output data/enhanced_frames

# Expected output:
# Processing frames |██████████████| 100.0% (10/10)
# ✓ Enhancement complete! Processed 10 frames
# ✓ Enhanced frames saved to: data/enhanced_frames

# ============================================================================
# STEP 12: LABEL YOUR FRAMES (STAGE 2 PREP)
# ============================================================================

# After enhancement, you need to manually label frames with bounding boxes.
# Choose one of these free tools:

# Option A: Roboflow (Online, easiest)
# 1. Go to https://roboflow.com
# 2. Create account (free tier available)
# 3. Create project → Upload enhanced frames
# 4. Annotate boxes with class names from data/classes.yaml
# 5. Export as "YOLO txt" format
# 6. Download and extract to: data/labels/

# Option B: CVAT (Self-hosted or online)
# 1. Go to https://www.cvat.ai (online) or https://github.com/opencv/cvat
# 2. Create project → Upload frames
# 3. Create detection task
# 4. Annotate bounding boxes
# 5. Export as "YOLO 1.1" format
# 6. Extract to: data/labels/

# Expected structure after labeling:
# data/labels/
# ├── frame_001.txt
# ├── frame_002.txt
# └── ...

# Each .txt file should contain (YOLO format):
# <class_id> <x_center_norm> <y_center_norm> <width_norm> <height_norm>
# Example:
# 0 0.45 0.52 0.15 0.18

# ============================================================================
# STEP 13: PREPARE DATASET (STAGE 2)
# ============================================================================

# In VS Code terminal:
python src/prepare_dataset.py --images data/enhanced_frames --labels data/labels --train-ratio 0.8

# Expected output:
# Validating labels...
# ✓ Valid images with labels: 8
# Train/Val split: 6 train, 2 val
# Copying training files... |████████| 100.0%
# Copying validation files... |██████| 100.0%
# ✓ Train/Val files organized
# ✓ DATASET READY FOR TRAINING

# ============================================================================
# STEP 14: TRAIN DETECTOR (STAGE 3)
# ============================================================================

# In VS Code terminal:
python src/train_detector.py --data data/dataset/data.yaml --model yolov8s --epochs 50 --device 0

# ⚠️ GPU REQUIRED or will be very slow on CPU
# Expected output:
# Loading base model: yolov8s
# Training config:
#   - Epochs: 50
#   - Image size: 640
#   - Batch size: auto
# [Training progress...]
# ✓ TRAINING COMPLETE
# ✓ Best weights saved to: models/detector/best.pt

# ============================================================================
# STEP 15: TRAIN CLASSIFIER (STAGE 4)
# ============================================================================

# In VS Code terminal:
python src/train_classifier.py --label-dir data/labels --image-dir data/enhanced_frames --model efficientnet_b0 --epochs 30 --device 0

# Expected output:
# Extracting fish crops from labeled images...
# ✓ Extracted 48 fish crops
# TRAINING SPECIES CLASSIFIER
# Training config:
#   - Model: efficientnet_b0
#   - Epochs: 30
# [Training progress with loss and accuracy...]
# ✓ TRAINING COMPLETE
# ✓ Best weights saved to: models/classifier/best.pt

# ============================================================================
# STEP 16: RUN FULL INFERENCE (STAGE 5)
# ============================================================================

# Now run inference on new frames:
python src/infer_pipeline.py --input data/raw_frames --detector models/detector/best.pt --classifier models/classifier/best.pt --output outputs/

# Expected output:
# Loading detector model...
# Loading classifier model...
# Found 10 images to process
# Processing frames |██████████████| 100.0%
# ✓ Detections saved to: outputs/detections.json
# ✓ Summary saved to: outputs/summary.csv
# INFERENCE COMPLETE
# Frames processed: 10
# Total detections: 47
# Species Summary:
#   bannerfish: 12
#   surgeonfish: 15
#   damselfish: 10
#   wrasse: 10

# ============================================================================
# STEP 17: VIEW RESULTS
# ============================================================================

# 1. Annotated images: data/outputs/annotated_frames/
#    (Open any image to see boxes + species labels)

# 2. JSON detections: outputs/detections.json
#    (Right-click → Open with → Text Editor)

# 3. CSV summary: outputs/summary.csv
#    (Right-click → Open with → Excel or Text Editor)

# ============================================================================
# WINDOWS TROUBLESHOOTING
# ============================================================================

# ISSUE: Python not found
# SOLUTION:
# - Check: python --version in Command Prompt
# - Add Python to PATH:
#   1. Search "Environment Variables" in Start menu
#   2. Click "Edit the system environment variables"
#   3. Click "Environment Variables..."
#   4. Under "User variables", click "Path" → Edit
#   5. Add: C:\Users\YourUsername\AppData\Local\Programs\Python\Python311
#   6. Click OK, restart Command Prompt

# ISSUE: venv activation fails (execution policy error)
# SOLUTION:
# In PowerShell (Run as Administrator):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then retry: .\venv\Scripts\Activate.ps1

# ISSUE: "pip is not recognized"
# SOLUTION:
# - Ensure Python is in PATH (see above)
# - Try: python -m pip install --upgrade pip
# - Then: python -m pip install -r requirements.txt

# ISSUE: CUDA/GPU not detected
# SOLUTION:
# - Install NVIDIA GPU drivers: https://www.nvidia.com/Download/driverDetails.aspx
# - Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
# - Use CPU mode (slower but works): --device -1

# ISSUE: "ModuleNotFoundError" when running scripts
# SOLUTION:
# - Ensure (venv) is active in terminal
# - Check: pip list (should show all required packages)
# - Reinstall: pip install -r requirements.txt

# ISSUE: Out of GPU memory during training
# SOLUTION:
# - Reduce batch size: --batch-size 16
# - Use smaller model: --model yolov8n
# - Use CPU: --device -1

# ISSUE: Slow training on CPU
# SOLUTION:
# - This is normal. GPU is 50-100x faster
# - For testing with CPU: --epochs 5 (instead of 50)
# - Install NVIDIA drivers + CUDA for GPU support

# ============================================================================
# CREATING CUSTOM RUN BUTTONS IN VS CODE (OPTIONAL)
# ============================================================================

# To add quick buttons for each stage:
# 1. Create file: .vscode/tasks.json
# 2. Paste this content (see separate file below)
# 3. Now you can press Ctrl+Shift+B to see run options

# ============================================================================
# NEXT STEPS
# ============================================================================

# 1. Collect and label more frames (200+ recommended for best results)
# 2. Retrain models with expanded dataset
# 3. Run inference on new batches of frames
# 4. Monitor outputs/detections.json for detection quality
# 5. Iterate: more data → better models → better results

# ============================================================================
# USEFUL LINKS
# ============================================================================

# Python: https://www.python.org/downloads/
# VS Code: https://code.visualstudio.com/
# Git: https://git-scm.com/download/win
# Roboflow: https://roboflow.com/
# CVAT: https://www.cvat.ai/
# YOLOv8 Docs: https://docs.ultralytics.com/
# PyTorch: https://pytorch.org/

print("✓ Setup guide complete! Follow the steps above to get started.")
print("✓ Questions? See the README.md file for more details.")
