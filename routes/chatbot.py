from flask import Blueprint, request, jsonify
from schemas.UserMessageSchema import UserMessageSchema, UserMessage
from controllers.ChatBotController import ChatBotController

chatbot_bp: Blueprint = Blueprint('chatbot', __name__)


#Creating route for communication with chatbot
@chatbot_bp.route('/', methods=['POST'])
@chatbot_bp.route('/chatbot', methods=['POST'])
def send_message_to_chatbot():
    #Checking if request data is valid
    data: dict = request.get_json()
    schema: UserMessageSchema = UserMessageSchema()
    try:
        user_message: UserMessage = schema.load(data)
    except:
        return jsonify({"Error message": "Invali request body format!"}), 400
    #Sendining data to controller
    res: dict = ChatBotController.send_message_to_chatbot(user_message=user_message)

    return jsonify(res)