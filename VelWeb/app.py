from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import smtplib
from email.message import EmailMessage

# === Flask Setup ===
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === Email Configuration ===
EMAIL_SENDER = 'your_email@gmail.com'  # change this
EMAIL_RECEIVER = 'careers@velmenni.com'
EMAIL_PASSWORD = 'your_app_password'   # Gmail App Password (not regular password)

# === Utility Functions ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email_with_attachment(file_path, filename):
    msg = EmailMessage()
    msg['Subject'] = 'New Resume Submission - Velmenni'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content('A new resume has been uploaded. Please find the attached file.')

    with open(file_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=filename)

    # Use Gmail SMTP with SSL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

# === API Endpoint ===
@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Send email with attachment
        send_email_with_attachment(file_path, filename)

        return jsonify({'message': 'Resume uploaded and emailed successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# === Run the Server ===
if __name__ == '__main__':
    app.run(debug=True)
