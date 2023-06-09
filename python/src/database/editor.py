# about editor RDS ----------------------------------------------------------------------

def getArticleIdByKeyword(cursor, keyword):
  query = "SELECT articles FROM keywords WHERE keyword = %s"
  cursor.execute(query,(keyword,))
  result = cursor.fetchall()
  return result

def getArticle(cursor, article_id):
  query = "SELECT * FROM article WHERE id = {}".format(int(article_id))
  cursor.execute(query)
  result = cursor.fetchall()
  return result

# process editor data ------------------------------------------
# 사용자 별 키워드로 키워드에 따른 기사 id들을 반환
def getUserInterestArticleIdDict(cursor, user_interest_dict):
    user_interest_article_id_dict = {}

    for user_id, keyword_list in user_interest_dict.items():
      article_id_dict = {}
      for keyword in keyword_list:
        user_article_id = getArticleIdByKeyword(cursor, keyword)

        if len(user_article_id) >= 1:
          article_id_to_array = user_article_id[0][0].split(" ")
          if len(article_id_to_array) >= 4:
            article_id_dict[keyword] = list(set(article_id_to_array[0:4]))
          else:
            article_id_dict[keyword] = list(set(article_id_to_array))

      if len(article_id_dict) >= 1:
          user_interest_article_id_dict[user_id] = article_id_dict
          
    return user_interest_article_id_dict
    

  # 기사 ids로 유저 별 article 정보 불러오기
def getArticleInfoDict(cursor, user_interest_article_id_dict):
  user_interest_article_dict = {}

  for user_id, article_id_dict in user_interest_article_id_dict.items():
    article_dict={}

    for keyword, article_id_list in article_id_dict.items():
      user_article_by_keyword_dict_list=[]

      for article_id in article_id_list:
        if article_id == "":
          pass
        else :
          article = getArticle(cursor,article_id)[0]
          user_article_by_keyword_dict_list.append(article)

      article_dict[keyword] = user_article_by_keyword_dict_list

    user_interest_article_dict[user_id] = article_dict
  
  return user_interest_article_dict

# 클라이언트에 정보 줄 때 사용-----------------------------------------------------------------------------------------
def getArticleInfoDictForClient(cursor, user_interest_article_id_dict):
  user_interest_article_dict = {}

  for user_id, article_id_dict in user_interest_article_id_dict.items():
    article_dict={}

    for keyword, article_id_list in article_id_dict.items():
      user_article_by_keyword_dict_list=[]

      for article_id in article_id_list:
        if article_id == "":
          pass
        else :
          article = getArticle(cursor,article_id)[0]
          article_obj = {}
          article_component = ["id", "time", "company", "title", "content", "image", "link"]
          for index, art in enumerate(article):
            article_obj[article_component[index]] = art

          user_article_by_keyword_dict_list.append(article_obj)

      article_dict[keyword] = user_article_by_keyword_dict_list

    user_interest_article_dict[user_id] = article_dict
  
  return user_interest_article_dict