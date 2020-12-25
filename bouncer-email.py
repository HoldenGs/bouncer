import smtplib, ssl, os
import boto3
from boto3.dynamodb.conditions import Attr, Key
from email.mime.text import MIMEText
import base64
from string import Template

# local imports
from google_auth import get_authenticated_google_service


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                    .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)


def check_for_new_members():

    sender_email = "codersleaguebcc@gmail.com"

    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    service = get_authenticated_google_service("gmail", "v1", SCOPES)

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('coders-league-members')

    # Send email to those whose 'welcome_email' field is 'no'
    members = table.scan(
            FilterExpression=Attr("welcome_email").eq("no")
    )
    for member in members['Items']:

        print(member)

        message = """\
Hello {},<br><br>
You are officially a member of Coder's League! Your information has been stored in our database. Though we will be sending \
all future email to your preferred email, we are sending this first email to your Peralta Email \
to verify you as a student at the Peralta Community College District.<br><br>\
Our most frequent mode of communication is Discord. To get on our Discord server, please use this \
<a href="https://discord.gg/jXxbvcHjTm">link</a><br><br> \
If you have further questions about the club, feel free to email codersleaguebcc@gmail.com or chat on Discord with \
an @officer.<br><br>
Coders League of Berkeley City College""".format(member['full_name'])
        
        receiver_email = "{}@cc.peralta.edu".format(member['student_id'])
        subject = "Welcome to Coders League!"
        message = create_message(sender_email, receiver_email, subject, message)
        res = send_message(service, "me", message)

        print(res)
        
        # update dynamo entry so we don't send anymore welcome emails to that member
        response = table.update_item(
            Key={
                'student_id': member['student_id']
            },
            UpdateExpression="set welcome_email = :g",
            ExpressionAttributeValues={
                    ':g': "yes"
            },
            ReturnValues="UPDATED_NEW"
        )

if __name__ == "__main__":
    check_for_new_members()