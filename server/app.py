from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        return make_response(messages, 200)
    
    elif request.method == 'POST':
        message_json = request.get_json()
        
        new_message = Message()
        for key, value in message_json.items():
            setattr(new_message, key, value)
        
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if not message:
        return make_response({'error': 'This is not available, our bad.'}, 404)
    else:
        if request.method == 'GET':
            return make_response(message, 200)
        elif request.method == 'PATCH':
            message_json = request.get_json()

            for key, value in message_json.items():
                setattr(message, key, value)
            
            db.session.commit()

            return make_response(message.to_dict(), 202)
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            return make_response({}, 204)
    
if __name__ == '__main__':
    app.run(port=5555)
