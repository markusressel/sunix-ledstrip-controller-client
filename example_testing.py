import asyncio

from sunix_ledstrip_controller_client.packets.requests import SetPowerRequest


#
# api1 = LEDStripControllerClient(keep_connections=True)
# device1 = Controller(api1, "192.168.2.33")
#
# api2 = LEDStripControllerClient(keep_connections=True)
# device2 = Controller(api2, "192.168.2.33")
#
# time.sleep(60)
#
# device1.turn_on()
# device1.turn_off()
# device1.turn_on()
# device1.turn_on()
#
# dt = datetime.now()
# device1.set_time(dt)
# device1.update_state()
# time = device1.get_time()
# device1.set_time(time)
#
# device1.set_rgb(5, 5, 5)
#
# colors = [(255, 0, 0, 255),
#           (0, 255, 0),
#           (0, 0, 255)]
# device1.set_ww(0, 0)
# device1.set_custom_function(colors, 250, TransitionType.Gradual)


async def connect():
    reader, writer = await asyncio.open_connection(
        '192.168.2.33', 5577)

    data = SetPowerRequest().get_data(True)
    send_message(data, writer)

    while True:
        await receive_messages(reader)


def send_message(message, writer):
    print(f'Send: {message!r}')
    writer.write(message)


async def receive_messages(reader):
    data = await reader.read(100)
    print(f'Received: {data!r}')


asyncio.run(connect())
