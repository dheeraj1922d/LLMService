from flask import Flask;
from flask import request , jsonify , json
from .service.messageService import MessageService
from kafka import KafkaProducer
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()
kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', '9092')
kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"
print("Kafka server is "+kafka_bootstrap_servers)
print("\n")
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route("/llm/v1/message" , methods=['POST'])
def handle_message():
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        return jsonify({'error': 'X-User-Id header is required'}), 400
    
    
    payload = request.get_json()  # Ensure proper extraction of JSON data
    if not payload or 'message' not in payload:
        return jsonify({'error': 'Missing "message" field in the request payload'}), 400
    
    # Extract the actual message string
    message = payload['message']
    
    # Process the message using the service
    try:
        result = messageService.process_message(message)

        if result is not None:
            serialized_result = result.serialize()
            serialized_result['user_id'] = user_id
            producer.send('expenses', serialized_result)
            return jsonify(serialized_result)
        else:
            return jsonify({'error': 'Invalid message format'}), 400
        
    except Exception as e:
        print(f"Error while processing message: {e}")
        return jsonify({'error': 'Internal server error'}), 500



@app.route('/', methods=['GET'])
def handle_get():
    return 'Hello world'


@app.route("/health" , methods=['GET'])
def helth_check():
    return "OK"

if __name__ == '__main__':
    app.run(host="localhost" , port=5000 , debug=True)