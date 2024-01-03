from opentrons_http_api.robot import Robot
from opentrons_http_api.utils.parameterize_protocol import parameterize_protocol, Parameter


ROBOT_IP = 'localhost'
PARAMS = (
    Parameter('num_flashes', 3),
    Parameter('delay_s', 0.2),
)


robot = Robot(ROBOT_IP)

# Doesn't work with f_out as a BytesIO or tempfile object
with open('_temp.py', 'w+b') as f_out:
    with open('../example_protocol_parameterized.py', 'rb') as f_in:
        parameterize_protocol(f_in, f_out, PARAMS)

    print(robot.upload_protocol(f_out))
