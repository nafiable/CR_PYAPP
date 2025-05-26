import os
from O365 import Account, Message, FileSystemTokenBackend

import configparser
import logging

logger = logging.getLogger(__name__)
from dotenv import load_dotenv, find_dotenv

def load_env_credentials():
    """Loads Microsoft 365 credentials from environment variables.
    Assumes environment variables are loaded from a .env file.

    Returns:
        dict: A dictionary containing the Microsoft 365 credentials
              (client_id, client_secret, tenant_id).
    """
    load_dotenv(find_dotenv()) # Load environment variables from .env file
def read_emails(query=None):
    Reads emails from a Microsoft 365 inbox using O365 library and credentials
    loaded from environment variables.

    Args:
        query (str, optional): An O365 query string to filter messages. Defaults to None.

    Returns:
        list: A list of O365 Message objects, or None if reading fails.
    """
        credentials = load_env_credentials()
        if not credentials or not all(credentials.values()):
            logger.error("Email credentials (MS365_CLIENT_ID, MS365_CLIENT_SECRET, MS365_TENANT_ID) not found in environment variables.")
            return None

        # Use FileSystemTokenBackend to manage tokens (requires initial authentication flow)
        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.json')

        # Account authentication (requires interactive authentication the first time)
        # Scopes depend on required permissions, 'basic' and 'message_all' are common for reading emails
        scopes = ['basic', 'message_all']
        account = Account(credentials, token_backend=token_backend)

        if account.authenticate(scopes=scopes):
            mailbox = account.mailbox()
            inbox = mailbox.inbox_folder()

            # Get messages with optional query
            messages = list(inbox.get_messages(query=query))
            logger.info(f"Read {len(messages)} emails from inbox.")
            return messages
        else:
            logger.error("O365 Authentication failed. Please run the authentication flow.")
            return None



def extract_attachments(email_message, output_dir: str) -> list:
    """
    Extracts attachments from an O365 email message and saves them to a directory.

    Args:
        email_message (Message): The O365 Message object containing the email.
        output_dir (str): The directory where attachments should be saved.

    Returns:
        list: A list of saved attachment file paths.
    """
    saved_attachments = []

    if isinstance(email_message, Message) and email_message.has_attachments:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for attachment in email_message.attachments:
            file_path = os.path.join(output_dir, attachment.name)
            attachment.save(file_path) # Use the save method provided by O365 attachment object
            saved_attachments.append(file_path)
            logger.info(f"Extracted attachment: {attachment.name}")
    return saved_attachments

def classify_email(email_message):
    Analyzes email subject and sender to suggest a classification group.

    Args:
        email_message (Message): The O365 Message object.

    Returns:
        str: A suggested classification group (e.g., 'Reports', 'Alerts', 'General'),
             or 'Unclassified' if no pattern is matched.
    """
    subject = email_message.subject.lower() if hasattr(email_message, 'subject') else ""
    sender_email = email_message.sender.address.lower() if hasattr(email_message, 'sender') and hasattr(email_message.sender, 'address') else ""

    if "report" in subject or "summary" in subject:
        return "Reports"
    elif "alert" in subject or "notification" in subject:
        return "Alerts"
    elif "urgent" in subject:
        return "Urgent"
    elif "newsletter" in subject or "marketing" in subject:
        return "Promotions"
    # Add more classification rules here based on your needs
    # Example based on sender domain or specific sender email
    # elif "specific_sender.com" in sender_email:
    #     return "Specific Group"

    return "Unclassified"


def send_email(recipient: str | list, subject: str, body: str) -> bool:
    """ Sends an email using the Microsoft 365 account configured in environment variables.

    Args:
        recipient (str or list): The email address(es) of the recipient(s).
        subject (str): The subject of the email.
        body (str): The body of the email. Returns:

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        credentials = load_env_credentials()
        if not credentials or not all(credentials.values()):
                logger.error("Email credentials (MS365_CLIENT_ID, MS365_CLIENT_SECRET, MS365_TENANT_ID) not found in environment variables.")
                return False

        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.json')
        account = Account(credentials, token_backend=token_backend)

        if account.authenticate(scopes=['basic', 'message_send']):
            m.to.add(recipient)
            m.subject = subject
            m.body = body
            m.send()
            return True
        else:
            logger.error("Authentication failed.")
            return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # Example structure - requires proper authentication flow
    try:
        credentials = load_env_credentials()
        if not credentials or not all(credentials.values()):
                logger.error("Email credentials (MS365_CLIENT_ID, MS365_CLIENT_SECRET, MS365_TENANT_ID) not found in environment variables.")
                return False

        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.json')
        account = Account(credentials, token_backend=token_backend)

        if account.authenticate(scopes=['basic', 'message_send']):
            m = account.new_message()
            m.to.add(recipient)
            m.subject = subject
            m.body = body
            for attachment_path in attachment_paths:
                try:
                    m.attachments.add(attachment_path)
                except FileNotFoundError:
                    logger.error(f"Attachment file not found: {attachment_path}")
                    # Decide whether to continue or fail here
            m.send()
        # else:
        #     logger.error("Authentication failed.")
        #     return False
    except Exception as e:
        logger.error(f"Error sending email with attachments: {e}")
        return False

# Note: To use the O365 library, you need to perform an initial authentication
# flow which typically involves opening a browser window to grant permissions.
# This initial setup is required before running the functions.
# Example:
# from O365 import Account, FileSystemTokenBackend
# credentials = {'client_id': 'YOUR_CLIENT_ID', 'client_secret': 'YOUR_CLIENT_SECRET'}
# token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.json')
# account = Account(credentials, token_backend=token_backend)
# # Define scopes based on operations you need (read, send, etc.)
# scopes = ['basic', 'message_all', 'message_send']
# if account.authenticate(scopes=scopes):
#     print("Authentication successful. Token saved to o365_token.json")
# else:
#     print("Authentication failed.")

if __name__ == '__main__':
    # Example usage (requires O365 setup and a valid token in o365_token.json):

    print("Email utility functions defined. Implementation details and authentication setup are required.")
    logger.info("Email utility functions defined. Implementation details and authentication setup are required.")
    # Read emails example:
    # logger.info("Attempting to read emails...")
    # emails = read_emails() # Reads all emails
    # if emails:
    #     logger.info(f"Read {len(emails)} emails.")
    #     for email in emails:
    #         classification = classify_email(email)
    #         logger.info(f"Email subject: {email.subject}, Classification: {classification}")
    #         # Example of extracting attachments from the first email
    #         # extract_attachments(email, 'attachments')

    # Example of reading emails with a query (e.g., emails from a specific sender)
    # logger.info("\nAttempting to read emails from specific sender...")
    # filtered_emails = read_emails(query="hasattachments eq true") # Example query
    # if filtered_emails:
    #      logger.info(f"Read {len(filtered_emails)} filtered emails.")

    # Send email example:
    # logger.info("\nAttempting to send email...")    # send_email('recipient@example.com', 'Test Email', 'This is a test email from the utility script.')

    # Send email with attachment example:
    # print("\nAttempting to send email with attachment...")
    # # Create a dummy file for attachment
    # with open('test_attachment.txt', 'w') as f:
    #     f.write('This is a test attachment.')
    # send_email_with_attachment('recipient@example.com', 'Test Email with Attachment', 'See attachment.', ['test_attachment.txt'])
    # # Clean up the dummy file if it was created
    # if os.path.exists('test_attachment.txt'):
    return None
