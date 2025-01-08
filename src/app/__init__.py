from flask import Flask;
from flask import request , jsonify
from service.messageService import MessageService

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()

@app.route("/llm/v1/message" , methods=['POST'])
def handle_message():
        # Extract the JSON payload from the request
    payload = request.get_json()  # Ensure proper extraction of JSON data
    if not payload or 'message' not in payload:
        return jsonify({'error': 'Missing "message" field in the request payload'}), 400
    
    # Extract the actual message string
    message = payload['message']
    
    # Process the message using the service
    try:
        result = messageService.process_message(message)
        print(f"Processed Result: {result}")
        return jsonify(result), 200
    except Exception as e:
        print(f"Error while processing message: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route("/health" , methods=['GET'])
def helth_check():
    return "OK"

if __name__ == '__main__':
    app.run(host="localhost" , port=5000 , debug=True)