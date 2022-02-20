import os
import config
from flask_socketio import SocketIO
from flask import Flask, request, jsonify


app = Flask(__name__)
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(CONFIG_TYPE)

socketio = SocketIO(app, logger=True, engineio_logger=True, message_queue='redis://localhost:6379')


@app.route('/write', methods=['POST'])
def write_results():
    data = request.json
    try:
        if not os.path.exists(os.path.join(config.basedir, config.Config.RESOURCE_DIR)):
            os.makedirs(os.path.join(config.basedir, config.Config.RESOURCE_DIR), exist_ok=False)
        with open(os.path.join(config.basedir, config.Config.RESOURCE_DIR, f"{data['resource_id']}.txt"), "w") as f:
            f.write("\n".join([str(d) for d in data['data']]))
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})


# Running on port 5001
if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5001, debug=True)
