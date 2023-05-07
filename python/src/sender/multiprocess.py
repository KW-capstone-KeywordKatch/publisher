import multiprocessing
import src.sender.smtp as smtp

# 사용자 별 이메일 폼 생성 : 멀티 프로세싱 적용
def create_email_templet_using_multiprocess(user_info_dict, user_interest_article_dict):
  manager = multiprocessing.Manager()
  html_list = manager.dict()
  proc_list = []

  for user_id, article_dict in user_interest_article_dict.items():
    mp = multiprocessing.Process(target=smtp.create_email_templet,args=(user_info_dict[user_id], user_id, html_list, article_dict))
    mp.start()
    proc_list.append(mp)
  
  for proc in proc_list:
    proc.join()

  return html_list

def send_email_using_multiprocess(html_list, user_info_dict):
  proc_list2 = []

  for user_id, user_info in user_info_dict.items():
    mp = multiprocessing.Process(target=smtp.send_email,args=(user_info, html_list[user_id]))
    mp.start()
    proc_list2.append(mp)

  for proc in proc_list2:
    proc.join()