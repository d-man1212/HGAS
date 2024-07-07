# Hand Gesture Recognition System

This system utilizes OpenCV and TensorFlow/Keras to enable real-time detection and recognition of hand gestures for authentication purposes. The system integrates a machine learning model trained using Teachable Machine for gesture classification and authentication. It achieves an approximate success rate of 80% in authenticating users based on their gestures.
Challenges include distinguishing between similar gestures, varying camera angles affecting recognition accuracy and environment variability.

## Table of Contents

- [Basic Information](#basic-information)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)

## Basic Information

This system detects and recognizes user-defined hand gestures captured via webcam. It leverages OpenCV to detect the user's hand, constructs a skeletal model of the hand, and uses a TensorFlow/Keras model trained with Teachable Machine to classify and store these gestures for authentication purposes. Data related to gestures and user authentication is stored in a MySQL database.

## Technologies Used

- **Tkinter**: Python's standard GUI (Graphical User Interface) library for creating the frontend interface.
- **OpenCV**: For real-time hand detection and skeletal modeling.
- **TensorFlow/Keras**: Used to train the machine learning model for gesture classification.
- **Teachable Machine**: Online tool utilized to create and train the model on a dataset of hand gestures.
- **MySQL**: Relational database used to store user authentication data and gesture information.

## Requirements

- Python 3.x
- OpenCV
- TensorFlow/Keras
- Mediapipe
- NumPy
- Pillow (PIL)
- Tkinter
- mysql-connector-python

## Installation

1. **Clone the repository:**

```git clone https://github.com/d-man1212/HGRS.git```

2. **Navigate to the project directory:**

```cd HGRS```

3. **Install dependencies:**

```bash
   pip install -r requirements.txt
```

4. **Run the application:**

```bash
   python main.py
```

## Usage

1. Ensure your camera is connected and accessible.
2. Upon running **main.py**, the application opens with a welcome screen offering options to register, login, or quit.
3. **Registration:** Users can register by inputting a username and performing a sequence of hand gestures.
4. **Login:** Existing users can login by providing their username and performing the same gestures used during registration.**
5. Successful authentication leads to a success screen displaying the username.

## Contributors

Thanks to the following contributors for their valuable contributions to this project:

- [Dharshan S (d-man1212)](https://github.com/d-man1212)
- [Padala Surya Sahith (SuryaSahith)](https://github.com/SuryaSahith)
- [Vishwa Kumar (SeveralSnipe)](https://github.com/SeveralSnipe)

Feel free to check out their profiles and contributions!