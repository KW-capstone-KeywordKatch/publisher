from flask import Flask
import emailSender
import db
import multiprocessing
import time
import psutil

app = Flask (__name__)

def memory_usage(message: str = 'debug'):
    # current process RAM usage
    p = psutil.Process()
    rss = p.memory_info().rss / 2 ** 20 # Bytes to MB
    print(f"[{message}] memory usage: {rss: 10.5f} MB")

# smtp 서버 연결
@app.before_first_request
def before_first_request():
    global conn, cursor
    conn, cursor = db.connectionRDS()

@app.route('/')
def hello_world():
  return 'hello'
    
# email로 기사 보내는 api
@app.route('/send')
def send_request():
  with app.app_context():
    manager = multiprocessing.Manager()
    msg_list = manager.dict()
    user_list = db.getAllUserInfo(cursor)

    start = int(time.time())

    proc_list = []

    memory_usage("start!!!")

    for i, user in enumerate(user_list):
      mp = multiprocessing.Process(target=emailSender.make_email_templet,args=(user, i, msg_list))
      mp.start()
      proc_list.append(mp)
    
    for proc in proc_list:
      proc.join()

    print("make form times:", int(time.time())-start)

    start2 = int(time.time())

    proc_list2 = []

    for i in range(len(user_list)):
      mp = multiprocessing.Process(target=emailSender.send_email,args=(user_list[i], msg_list[i]))
      mp.start()
      memory_usage("process:{i}")
      proc_list2.append(mp)

    for proc in proc_list2:
      proc.join()

    end = int(time.time())

    print("send run time(sec) :", end - start2)
    
    print("total run time(sec) :", end - start)

    return "end"
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)