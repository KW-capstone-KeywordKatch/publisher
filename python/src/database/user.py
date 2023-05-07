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
  query = "SELECT * FROM user_interest WHERE user_id IN {}".format(tuple(user_ids))
  
  cursor.execute(query)
  result = cursor.fetchall()
  return result

# process user data --------------------------------------------------

# 사용자의 정보 반환 ( user_id : [이메일, 닉네임]의 딕셔너리, user_id 리스트 )
def getUserInfoDictAndUserIdList(user_cursor):
  user_infos = getAllUserInfo(user_cursor)
  
  user_info_dict = {}
  user_id_list = []

  for user_info in user_infos:
    tmp = list(user_info)
    user_info_dict[tmp[0]] = [tmp[1],tmp[2]]
    user_id_list.append(tmp[0])

  return user_info_dict, user_id_list

# 사용자 별 관심사 반환 ( user_id : [관심사1, 관심사2...] 의 딕셔너리 )
def getUserInterestDict(user_cursor, user_id_list):
    user_interests = getUserInterest(user_cursor, user_id_list)
    user_interest_dict = {}

    for user_interest in user_interests:
      if (user_interest[0] in user_interest_dict):
        user_interest_dict[user_interest[0]].append(user_interest[1])
      else :
        user_interest_dict[user_interest[0]] = [user_interest[1]]
    
    return user_interest_dict