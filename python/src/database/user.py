from datetime import datetime, timedelta

# about user RDS ----------------------------------------------------------------------
def getAllUserInfo(cursor):
  query = "SELECT * FROM user_info"

  cursor.execute(query)
  result = cursor.fetchall()
  return result

def getAllUserIdAndEmail(cursor):
  query = "SELECT user_id, email FROM user_info"

  cursor.execute(query)
  result = cursor.fetchall()
  return result

def getUserInterest(cursor, user_ids):
  if len(user_ids) > 1:
    query = "SELECT * FROM user_interest WHERE user_id IN {}".format(tuple(user_ids))
    cursor.execute(query)
    result = cursor.fetchall()
    return result
  else :
    query = "SELECT * FROM user_interest WHERE user_id = {}".format(int(user_ids[0]))
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# process user data -----------------------------------------------------------------

# 사용자의 정보 반환 ( user_id : [이메일, 닉네임]의 딕셔너리, user_id 리스트 )
# 사용자 전송 시간 까지 확인함
def getUserData(user_cursor):
  user_infos = getAllUserInfo(user_cursor)
  
  user_info_dict = {}
  user_id_list = []

  if len(user_infos) == 0 :
    return user_info_dict, user_id_list
  
  '''
    for user_info in user_infos:
    user_data = list(user_info)
    is_sendable_user = checkUserSendTime(user_data)

    if is_sendable_user:
      user_info_dict[user_data[0]] = [user_data[1],user_data[3]]
      user_id_list.append(user_data[0])
  '''

  for user_info in user_infos:
    user_data = list(user_info)
    user_info_dict[user_data[0]] = [user_data[1],user_data[3]]
    user_id_list.append(user_data[0])

  print("전송 유저 : ",user_info_dict)   

  return user_info_dict, user_id_list

# 사용자 별 관심사 반환 ( user_id : [관심사1, 관심사2...] 의 딕셔너리 )
def getUsersInterest(user_cursor, user_id_list):
    user_interests = getUserInterest(user_cursor, user_id_list)

    user_interest_dict = {}

    # dict에 key : user_id 가 없으면 추가, 있으면 해당 value(interest)에 이어 붙이기
    for user_interest in user_interests:
        if user_interest[0] in user_interest_dict:
            user_interest_dict[user_interest[0]].append(user_interest[1])
        else:
            user_interest_dict[user_interest[0]] = [user_interest[1]]
  
    return user_interest_dict

# 사용자 send_time 확인하기
def checkUserSendTime(user):
  user_nickname = user[3]
  user_send_time = user[2]

  if user_send_time == None:
    return False
  # 한국 시간 = 미국시간 + 9h
  current_time = datetime.now() + timedelta(hours=9)
  
  modify_time = current_time.time().strftime("%H:%M")
  
  user_send_time_str_list = user_send_time.split(" ")
  user_send_time_list = []

  for user_time_str in user_send_time_str_list:
    user_time = datetime.strptime(user_time_str, "%H%M").time().strftime("%H:%M")
    user_send_time_list.append(user_time)

  print(user_nickname,"님의 이메일 전송시간 확인 중..")
  print(modify_time,"and",user_send_time_list)
  if modify_time in user_send_time_list:
    print("이메일 전송 가능")
    return True
  else :
    print("이메일 전송 불가능")
    return False
    