from opentrons_http_api.robot import Robot


ROBOT_IP = 'localhost'


robot = Robot(ROBOT_IP)
for run in robot.runs():
    print(run)
