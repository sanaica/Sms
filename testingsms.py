#from twilio.rest import Client
#account_sid = '' #your account sid
#auth_token = '' #your auth token
#client = Client(account_sid, auth_token)
#message = client.messages.create(
#  messaging_service_sid='',
#  body='HI123', #msg body
#  to='' #the number to which you want to send the message
#)
#print(message.sid) #prints the message

import os
from flask import Flask, request, jsonify, render_template_string
from twilio.rest import Client
import re

app = Flask(__name__)


# LOAD YOUR CREDENTIALS SECURELY FROM ENVIRONMENT VARIABLES
# ========================================================

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

# ADD THIS LINE FOR DEBUGGING
print(f"--- VERCEL DEBUG --- Account SID Used: '{account_sid}'")

client = Client(account_sid, auth_token)

def is_valid_phone_number(phone):
    # Basic phone number validation
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', ''))

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    try:
        data = request.json
        parent_number = data.get('parent_number', '').strip()
        
        if not parent_number:
            return jsonify({'success': False, 'error': 'Parent number is required'}), 400
        
        # Clean and validate phone number
        cleaned_number = parent_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not cleaned_number.startswith('+'):
            cleaned_number = '+1' + cleaned_number  # Assuming US numbers if no country code
        
        if not is_valid_phone_number(cleaned_number):
            return jsonify({'success': False, 'error': 'Invalid phone number format'}), 400
        
        # Send the SMS
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body='Child is in danger',
            to=cleaned_number
        )
        
        return jsonify({
            'success': True, 
            'message_sid': message.sid,
            'sent_to': cleaned_number
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# HTML Template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emergency SMS Alert System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
            max-width: 450px;
            width: 100%;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .title {
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }

        .alert-icon {
            font-size: 4em;
            color: #ff4757;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        .form-group {
            margin-bottom: 25px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
            font-size: 1.1em;
        }

        .input-container {
            position: relative;
        }

        input[type="tel"] {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 1.1em;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }

        input[type="tel"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }

        .send-btn {
            background: linear-gradient(45deg, #ff4757, #ff6b7a);
            color: white;
            border: none;
            padding: 16px 40px;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
        }

        .send-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 71, 87, 0.5);
        }

        .send-btn:active {
            transform: translateY(-1px);
        }

        .send-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .message {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            font-weight: 500;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        }

        .message.show {
            opacity: 1;
            transform: translateY(0);
        }

        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .loading {
            display: none;
            margin-top: 20px;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .help-text {
            font-size: 0.9em;
            color: #777;
            margin-top: 8px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="alert-icon">🚨</div>
        <h1 class="title">Emergency Alert</h1>
        <p class="subtitle">Send urgent notification to parent</p>
        
        <form id="smsForm">
            <div class="form-group">
                <label for="parentNumber">Parent's Phone Number</label>
                <div class="input-container">
                    <input 
                        type="tel" 
                        id="parentNumber" 
                        name="parentNumber" 
                        placeholder="+1 (555) 123-4567"
                        required
                    >
                </div>
                <div class="help-text">Include country code (e.g., +1 for US)</div>
            </div>
            
            <button type="submit" class="send-btn" id="sendBtn">
                Send Emergency Alert
            </button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Sending message...</p>
        </div>
        
        <div id="message" class="message"></div>
    </div>

    <script>
        document.getElementById('smsForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const parentNumber = document.getElementById('parentNumber').value.trim();
            const sendBtn = document.getElementById('sendBtn');
            const loading = document.getElementById('loading');
            const messageDiv = document.getElementById('message');
            
            if (!parentNumber) {
                showMessage('Please enter a parent\\'s phone number', 'error');
                return;
            }
            
            // Show loading state
            sendBtn.disabled = true;
            loading.style.display = 'block';
            messageDiv.classList.remove('show');
            
            try {
                const response = await fetch('/send_sms', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        parent_number: parentNumber
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage(`Emergency alert sent successfully to ${data.sent_to}`, 'success');
                    document.getElementById('parentNumber').value = '';
                } else {
                    showMessage(`Error: ${data.error}`, 'error');
                }
                
            } catch (error) {
                showMessage('Failed to send message. Please try again.', 'error');
                console.error('Error:', error);
            } finally {
                // Hide loading state
                sendBtn.disabled = false;
                loading.style.display = 'none';
            }
        });
        
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = text;
            messageDiv.className = `message ${type}`;
            messageDiv.classList.add('show');
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                messageDiv.classList.remove('show');
            }, 5000);
        }
        
        // Format Indian phone number as user types
        document.getElementById('parentNumber').addEventListener('input', function(e) {
            let value = e.target.value.replace(/\\D/g, '');
            
            // Handle Indian number formatting
            if (value.startsWith('91') && value.length > 2) {
                // Format as +91 XXXXX XXXXX
                if (value.length <= 7) {
                    value = `+91 ${value.slice(2)}`;
                } else {
                    value = `+91 ${value.slice(2, 7)} ${value.slice(7, 12)}`;
                }
            } else if (value.length === 10 && (value.startsWith('6') || value.startsWith('7') || value.startsWith('8') || value.startsWith('9'))) {
                // Format 10-digit number as +91 XXXXX XXXXX
                value = `+91 ${value.slice(0, 5)} ${value.slice(5, 10)}`;
            } else if (value.startsWith('91')) {
                // Handle partial 91 prefix
                value = `+${value}`;
            } else if (value.length > 0) {
                // For other international numbers, just add +
                value = `+${value}`;
            }
            
            e.target.value = value;
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)