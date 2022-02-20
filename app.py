from flask import Flask, session, copy_current_request_context
from flask_socketio import SocketIO, disconnect
from _celery import make_celery
from utils import send_webhook

# all the app configs gets loaded during app initialization
# i.e. from __init__ file
app = Flask(__name__)
socketio = SocketIO(app)
client = make_celery(app.name)

# a global dict get maintained to maintain results from ancillary service.
# Note that the primary resource id and it's data gets
# deleted once the data is stored in file. so this dict will not grow large
results = {}


@client.task(bind=True)
def get_payload_lengths(self, payload):
    """
    :param self:
    :param payload: payload string/bytes
    :return: list of len of each word in payload
    """
    return [len(word) for word in str(payload).split(" ")]


@socketio.on('collect_packet')
def collect_packet(packet):
    """
    Receives resource packets, passes to ancillary task to get length of each word in payload
    :param packet: The received packet
    :return:
    """

    # await call

    packet_index = packet['data_packet_index']
    packet_resource_id = packet['primary_resource_id']
    primary_resource_id = results.get(packet_resource_id, None)

    ancillary_result = get_payload_lengths.apply_async(args=[packet['payload']]).get()

    if primary_resource_id is None:
        results[packet_resource_id] = {}

    # if its the last chunk, collect all the packets for that resource, sort them
    # as they might be in order. Collate output data for that resource and call webhook
    if packet['last_chunk']:
        results[packet_resource_id][packet_index] = ancillary_result
        resource_packets = results.pop(packet_resource_id)
        sorted_packets = dict(sorted(resource_packets.items()))
        flat_output = [value for values in sorted_packets.values() for value in values]
        send_webhook(packet_resource_id, flat_output)
    else:
        # it's not the end of packets for the given primary resource yet, so keep collecting
        results[packet_resource_id][packet_index] = ancillary_result
    socketio.emit('on_packet_produced', packet)


def task_completed(result):
    """
    Can celery task notify server/client when its done?
    The idea was to use the even to let task notify that it is done with
    processing. But looks like we can't emit from tasks
    :param result:
    :return:
    """
    print(f"Task completed : {result}")


@socketio.on('disconnect_request')
def disconnect_request():
    """
    On disconnect event
    :return:
    """

    @copy_current_request_context
    def can_disconnect():
        disconnect()

    socketio.emit('on_connection_closed',
                  {'data': 'Disconnected!', 'count': session['receive_count']},
                  callback=can_disconnect)


if __name__ == "__main__":
    import flask_cors

    flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
    socketio.run(app, debug=True)
