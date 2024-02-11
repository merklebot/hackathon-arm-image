import os
import time
import math
from spot_controller import SpotController
from collections import defaultdict

ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']

import time

def main():
    #example of using micro and speakers
    print("Start recording audio")
    sample_name = "cha.mp4"
    cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    print(cmd)
    os.system(cmd)
    print("Playing sound")
    os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
    # Capture image
    import cv2
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()
    import whisper

# Define the path to your audio file
    audio_file_path = 'cha.mp4'

    # Initialize the Whisper model
    model = whisper.load_model("base")  # You can choose a different model size as needed
#hello
    # Transcribe the audio file
    result = model.transcribe(audio_file_path)
    spot=SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP)
# Function to search for words and return timestamps
    def find_keywords_in_transcription(transcription, keywords):
        timestamps = defaultdict()
        for segment in transcription['segments']:
            for word in keywords:
                if word in segment['text']: 
                    if word=='left':
                        timestamps[segment['start']]==spot.move_left()
                    if word=='right':
                        timestamps[segment['start']]==spot.move_right()

# Define the keywords you're looking for
    keywords = ['left', 'right','take it back','smooth']

    # Find and print the timestamps for the keywords
    timestamps = find_keywords_in_transcription(result, keywords)
    sorted_timestamps_commands = sorted(timestamps_commands.items())

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:

            spot_controller = SpotController(username='your_username', password='your_password', robot_ip='spot_robot_ip')
            current_time = time.time()

            for timestamp, command in sorted_timestamps_commands:
    # Calculate how long to wait before executing the command
                wait_time = timestamp - current_time
    
    # If the wait time is positive, sleep until the timestamp
                if wait_time > 0:
                    print(f"Waiting {wait_time} seconds to execute command.")
                    time.sleep(wait_time)
                
                # Execute the command. This example simply evaluates a string as Python code.
                # If your commands are function names, you might instead call the function directly.
                exec(command)
                
                # Update the current time to the timestamp after executing the command
                # If commands are sequential without real-time constraint, remove this line
                current_time = timestamp

            # Define the parameters for walking in a circle
            circle_radius = 1.0  # radius of the circle in meters
            angular_velocity = 0.2  # angular velocity in rad/s
            
            # Calculate the linear velocity needed to maintain a constant angular velocity
            linear_velocity = angular_velocity * circle_radius

            # Calculate the time to complete one full circle
            circle_duration = 2 * math.pi * circle_radius / linear_velocity

            # Start walking in a circle
            spot_controller.move_by_velocity_control(v_x=linear_velocity, v_rot=angular_velocity, cmd_duration=circle_duration)
            spot_controller.bow(pitch=2)



if __name__ == '__main__':
    main()

