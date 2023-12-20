from opentrons import protocol_api


metadata = {
    'protocolName': 'Turn rail lights on',
    'author': 'morefigs',
    'description': 'Turns the rail lights of the OT-2 on',
}

requirements = {'robotType': 'OT-2', 'apiLevel': '2.15'}


def run(ctx: protocol_api.ProtocolContext):
    ctx.set_rail_lights(True)
