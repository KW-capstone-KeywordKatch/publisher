from flask import Flask
import emailSender

app = Flask (__name__)

# smtp 서버 연결
@app.before_first_request
def before_first_request():
    global smtp_connect
    smtp_connect = emailSender.connect_smtp_server()

@app.route('/')
def hello_world():
  return 'hello'

# email로 기사 보내는 api
@app.route('/send/<email>')
def send_request(email):
  smtp_server = smtp_connect
  send_html = emailSender.send_email(smtp_server, email)
  return send_html

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)