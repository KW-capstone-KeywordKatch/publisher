import pymysql
import sys
import logging
import os
 
# connect with RDS -----------------------------------------------------------------------
def connectUSERRDS():
  try:
    conn=pymysql.connect(host=os.getenv('USER_HOST'), user=os.getenv('USER_USERNAME'), passwd=os.getenv('USER_PASSWORD'), db=os.getenv('USER_DATABASE'), port=int(os.getenv('RDS_PORT')), use_unicode=True, charset="utf8")
    cursor = conn.cursor()
  except Exception as e:
    logging.error("RDS연결 실패:"+str(e))
    sys.exit(1)

  return conn, cursor

def connectARTICLERDS():
  try:
    conn=pymysql.connect(host=os.getenv('ARTICLE_HOST'), user=os.getenv('ARTICLE_USERNAME'), passwd=os.getenv('ARTICLE_PASSWORD'), db=os.getenv('ARTICLE_DATABASE'), port=int(os.getenv('RDS_PORT')), use_unicode=True, charset="utf8")
    cursor = conn.cursor()
  except Exception as e:
    logging.error("RDS연결 실패:"+str(e))
    sys.exit(1)

  return conn, cursor

def connectLOCALRDS():
  try:
    conn=pymysql.connect(host=os.getenv('LOCAL_HOST'), user=os.getenv('LOCAL_USERNAME'), passwd=os.getenv('LOCAL_PASSWORD'), db=os.getenv('LOCAL_DATABASE'), port=int(os.getenv('RDS_PORT')), use_unicode=True, charset="utf8")
    cursor = conn.cursor()
  except Exception as e:
    logging.error("RDS연결 실패:"+str(e))
    sys.exit(1)

  return conn, cursor