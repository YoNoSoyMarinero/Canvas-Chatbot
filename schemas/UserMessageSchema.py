from marshmallow import Schema, fields, post_load

class UserMessage:
    def __init__(self, user_name, user_email, message_text, token):
        self.user_name: str = user_name
        self.user_email: str = user_email
        self.message_text: str = message_text
        self.token: str = token

    def __repr__(self):
        return f'User name:{self.user_name}\nUser email:{self.user_email}\nMessage text:{self.message_text}'

class UserMessageSchema(Schema):
    user_name: str = fields.String(required=True)
    user_email: str = fields.String(required=True)
    message_text: str = fields.String(required=True)
    token: str = fields.String(required=True)

    @post_load()
    def create_user_message(self, data, **kwargs):
        return UserMessage(**data)