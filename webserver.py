from flask import Flask, request, jsonify
from adafruit_motorkit import MotorKit
import time

app = Flask(__name)

# Create a dictionary to store the robot's current state eg. stopped
robot_state = "stopped"

# Initialize the MotorKit
kit = MotorKit(0x40)

# Define movement functions
def move_forward():
    kit.motor1.throttle = 0.77
    kit.motor2.throttle = 0.75
    robot_state = "moving forward"
def move_backward():
    kit.motor1.throttle = -0.80
    kit.motor2.throttle = -0.76
    robot_state = "moving backward"

def turn_left():
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = -0.75
    robot_state = "turning left"

def turn_right():
    kit.motor1.throttle = -0.76
    kit.motor2.throttle = 0.75
    robot_state = "turning right"

def stop_robot():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    robot_state = "stopped"
#endpoint to receive movement commands
@app.route('/move', methods=['POST'])
def move_robot():
    global robot_state
    data = request.get_json()
    direction = data.get('direction') #direction sent from send_command()
    # move robot based on the 'direction' received
    if direction == 'forward':
        move_forward()
    elif direction == 'backward':
        move_backward()
    elif direction == 'left':
        turn_left()
    elif direction == 'right':
        turn_right()
    elif direction == 'stop':
        stop_robot()

    return jsonify({'message': f"Robot is now {robot_state}"}) #prints what state the robot is currently in.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #must be using 0.0.0.0 because this ensures that the server can be accessed from other computers. 
#the default 127.0.0.1 doesnt allow other computers except the one running the server to process requests.
