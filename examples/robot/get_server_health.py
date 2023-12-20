from wip.robot import Robot


ROBOT_IP = 'localhost'


robot = Robot(ROBOT_IP)
print(robot.health())
