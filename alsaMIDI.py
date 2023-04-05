import time
from alsa_midi import SequencerClient, READ_PORT, NoteOnEvent, NoteOffEvent

client = SequencerClient("my client")
port = client.create_port("output", caps=READ_PORT)
print(f"port = {port}")
dest_port = client.list_ports(output=True)[0]
print(f"dest_port = {dest_port}")
port.connect_to(dest_port)
print(f"port = {port}")
event1 = NoteOnEvent(note=60, velocity=64, channel=0)
client.event_output(event1)
client.drain_output()
print(f"send note 1")
time.sleep(1)
event2 = NoteOffEvent(note=60, channel=0)
client.event_output(event2)
client.drain_output()
print(f"send note 2")