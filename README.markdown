# Music Recommendation System

## Overview

This project is a **Music Recommendation System** that uses facial and hand gesture recognition to detect a user's emotions and recommend songs based on the detected emotion, preferred language, and favorite singer. The system leverages a pre-trained machine learning model, MediaPipe for real-time landmark detection, and Flask for the web interface. It integrates with YouTube to suggest relevant songs.

## Features

- **Emotion Detection**: Detects emotions (e.g., happy, sad, fear) using facial landmarks and hand gestures captured via webcam.
- **Personalized Recommendations**: Recommends songs based on the user's detected emotion, preferred language, and favorite singer.
- **Real-Time Video Processing**: Streams webcam feed with overlaid emotion labels and landmarks using MediaPipe.
- **Web Interface**: Built with Flask, allowing users to interact with the system, start/stop video, and input preferences.
- **YouTube Integration**: Opens YouTube search results with tailored song recommendations.

## Technologies Used

- **Python**: Core programming language.
- **Flask**: Web framework for the user interface and backend.
- **MediaPipe**: For real-time face and hand landmark detection.
- **OpenCV**: For video capture and processing.
- **Keras**: For loading and using the pre-trained emotion detection model.
- **NumPy**: For numerical computations.
- **YouTube**: For song recommendations via search queries.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8+
- pip (Python package manager)
- A webcam for video input

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/maaz-alam04/Music-Recommendation-System.git
   cd Music-Recommendation-System
   ```

2. **Set Up a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` includes:

   ```
   flask
   opencv-python
   mediapipe
   numpy
   keras
   tensorflow
   ```

4. **Download the Pre-Trained Model**:

   - Ensure `model.h5` (pre-trained Keras model) and `labels.npy` (emotion labels) are in the project directory.

## Usage

1. **Run the Application**:

   ```bash
   python app.py
   ```

   The Flask server will start, and the app will be accessible at `http://127.0.0.1:5000`.

2. **Interact with the Web Interface**:

   - Open the provided URL in a browser.
   - Allow webcam access to start the video feed.
   - The system will display detected emotions on the video feed.
   - Select a language and singer, then click "Recommend" to get song suggestions.
   - Click "Stop Video" to release the webcam.

3. **Song Recommendations**:

   - Based on the detected emotion, the system generates a YouTube search query.
   - For "sad" or "fear" emotions, it recommends uplifting/motivational songs.
   - For other emotions, it matches songs to the detected emotion.

## File Structure

- `app.py`: Main Flask application with emotion detection, video streaming, and recommendation logic.
- `model.h5`: Pre-trained Keras model for emotion detection.
- `labels.npy`: Array of emotion labels.
- `templates/index.html`: HTML template for the web interface.
- `requirements.txt`: List of Python dependencies.

## How It Works

1. **Emotion Detection**:

   - The webcam captures video frames, which are processed using OpenCV.
   - MediaPipe extracts facial and hand landmarks.
   - Landmarks are normalized and fed into the pre-trained Keras model to predict emotions.
   - The detected emotion is displayed on the video feed.

2. **Video Streaming**:

   - Flask streams the processed video frames with landmarks and emotion labels to the browser.

3. **Song Recommendation**:

   - Users input their preferred language and singer via the web interface.
   - The system constructs a YouTube search query based on the detected emotion, language, and singer.
   - The query is opened in a new browser tab.

## Limitations

- Requires a webcam and good lighting for accurate emotion detection.
- The pre-trained model may not cover all possible emotions.
- Internet connection is needed for YouTube recommendations.
- Limited to YouTube for song suggestions.

## Future Improvements

- Expand the emotion detection model to recognize more emotions.
- Integrate with music streaming platforms (e.g., Spotify, Apple Music).
- Add support for playlist generation.
- Improve the UI/UX with a more modern design.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, please contact Maaz Alam or open an issue on GitHub.