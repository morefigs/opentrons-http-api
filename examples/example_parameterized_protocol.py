from opentrons import protocol_api


metadata = {
    'protocolName': 'Example parameterized protocol',
    'author': 'morefigs',
    'description': 'A protocol with replaceable parameters',
}

requirements = {'robotType': 'OT-2', 'apiLevel': '2.15'}


# Parameters
NUM_FLASHES = '''num_flashes'''
DELAY_S = '''delay_s'''


def run(ctx: protocol_api.ProtocolContext, num_flashes: int = NUM_FLASHES, delay_s: float = DELAY_S):
    for _ in range(num_flashes):
        ctx.set_rail_lights(True)
        ctx.delay(delay_s)
        ctx.set_rail_lights(False)
        ctx.delay(delay_s)
