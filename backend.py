from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

@app.route('/send_emails', methods=['POST'])
def send_emails():
    try:
        data = request.get_json()
        emails = data.get('emails')
        content = data.get('content')
        user_ids = data.get('user_ids')

        if not emails or not content:
            return jsonify({'error': 'Emails and content are required'}), 400

        sender_email = 'syhmecollection@gmail.com'
        sender_password = 'pviu yygr kcdb xzzm'

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        for i, email in enumerate(emails):
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = 'Syhme Weekly Newsletter'
            # msg['Subject'] = f'Dear {email} - Syhme Weekly Newsletter'
            
            # HTML content as email template
            html_content = content
            
            # Construct unsubscribe link with the email address
            unsubscribe_link = f'<a href="https://syhme.com/unsubscribe?email={email}&userId={user_ids[i]}">Unsubscribe</a>'
            html_content += f'<br><br>{unsubscribe_link}'
            
            msg.attach(MIMEText(html_content, 'html'))

            server.sendmail(sender_email, email, msg.as_string())
            

        server.quit()
        return jsonify({'message': 'Emails sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
