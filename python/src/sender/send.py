import src.database.user as user
import src.database.editor as editor
import src.sender.multiprocess as multi
import time
from datetime import datetime, timedelta

def send_email_each_time(user_cursor, editor_cursor):
  # 1. 사용자 별 전송할 기사 정보 받아오기
  # dict = {user_id:[email, nickname], ...} : 이메일 전송 때 사용함
  # list = [user_id1, user_id2, ...] : 사용자의 키워드 리스트 받아올 때 사용
  user_info_dict, user_id_list = user.getUserData(user_cursor)

  if len(user_id_list) == 0 :
    return [False, "No user in database or sendable user is not existed", {}]

  # { user_id : [key1, key2, key3...], ...} : 사용자 별 키워드에 따른 기사id들을 받아 올 때 사용
  user_interest_dict = user.getUsersInterest(user_cursor, user_id_list)

  if len(user_interest_dict) == 0 :
    return [False, "No keyword entered by all users.", {}]

  # {user_id : {keyword:["article_id1","article_id2"...]}, ...} : 키워드 별 기사 내용 받아 올 때 사용
  user_interest_article_id_dict = editor.getUserInterestArticleIdDict(editor_cursor, user_interest_dict)

  if len(user_interest_article_id_dict) == 0:
    return [False, "No article ids about the keyword.", {}]

  # {user_id : {keyword:[[기사정보1..],[기사정보2..], ...], ...}, ...} : 사용자 별 메일 보낼 때 사용
  user_interest_article_dict = editor.getArticleInfoDict(editor_cursor,  user_interest_article_id_dict)

  sendable_user_info_dict = {}

  for user_id in user_info_dict.keys():
    if user_interest_article_dict.get(user_id) is not None:
      sendable_user_info_dict[user_id] = user_info_dict[user_id]

  # 2. 사용자 별 이메일 폼 생성
  html_list = multi.create_email_templet_using_multiprocess(sendable_user_info_dict, user_interest_article_dict)

  # 3. 이메일 전송
  start_send_email = int(time.time())

  multi.send_email_using_multiprocess(html_list, sendable_user_info_dict)

  end = int(time.time())

  print("total run time(sec) :", end - start_send_email)

  return [True, "", sendable_user_info_dict]