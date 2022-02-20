import uuid
import random
from faker import Faker
from config import Config
from faker.providers import BaseProvider
from socketIO_client import SocketIO, LoggingNamespace


class PacketProvider(BaseProvider):
    @staticmethod
    def produce_packet(resource_id, packet_index, is_last_chunk):
        packet = {
            'primary_resource_id': resource_id, 'payload': _faker.sentence(), 'data_packet_index': packet_index,
            'last_chunk': is_last_chunk
        }
        return packet


def on_connection_closed():
    print(f"Connection closed...")


def on_packet_produced(args):
    print(f"Packet produced: {args}")


def produce_bunch_tasks():
    """
    Use faker to demonstrate producing packets for app to consume.
    :return:
    """
    print(f"Simulating {num_resource_to_simulate-1} resources with random length")
    for _ in range(1, num_resource_to_simulate):
        batch_id = str(uuid.uuid4())
        n = random.randint(Config.MIN_NBR_PKTS, Config.MAX_NBR_PKTS)
        for idx in range(n):
            pkt = PacketProvider.produce_packet(batch_id, idx, idx == n - 1)
            socketIO.emit('collect_packet', pkt)
            socketIO.wait(seconds=Config.WAIT_TIME)
            yield idx, pkt


_faker = Faker('en_US')
_faker.seed_instance(0)
_faker.add_provider(PacketProvider)
num_resource_to_simulate = random.randint(1,5)

if __name__ == "__main__":
    socketIO = SocketIO('localhost', 5000, LoggingNamespace)
    socketIO.on('on_connection_closed', on_connection_closed)
    socketIO.on('on_packet_produced', on_packet_produced)
    for index, packet in produce_bunch_tasks():
        pass
