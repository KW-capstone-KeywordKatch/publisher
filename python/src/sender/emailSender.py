import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from flask import render_template
import logging
import time


def connect_smtp_server():
  print("start connection")
  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  # 보내는 사람의 email - 임시로 넣음. 나중에 따로 계정 파서 넣기
  # 구글 앱 비밀번호 - 2차 인증 - 앱 비밀번호
  # SMTP 세션 생성
  smtp_connect = smtplib.SMTP(smtp_server, smtp_port)
  smtp_connect.starttls()
  smtp_connect.login(os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'))

  print("end connection")
  
  return smtp_connect

def make_email_templet(user, idx, msg_list):
  recv_email = user[1]

  msg = MIMEMultipart("alternative")
  # 여기에 뉴스 보내는 날짜 추가하기 ( 서버에서 같이 받기 or 현재 날짜 보내기)
  # 사용자가 받는 메일 제목
  msg["Subject"] = "오늘의 기사"
  # 표시 될 발송자 이름
  msg["From"] = formataddr(("KeywordKatch", os.getenv('ADMIN_EMAIL')))
  msg["To"] = recv_email

  # email로 db에 접근 -> 필요한 정보 읽어오기 -> 아래 templete에 저장하기
  # title : 30자 이상 -> 27번째에서 slice + "..."
  # content : 275자 이상 -> 270번째에서 slice + "..."
  # etc_title : 36자 이상 -> 33자에서 짜르기
  # news 요소 : unlone, title, content, src, picture

  # user의 관심사로 기사 긁어와서 아래 html에 박기

  # 전송하는 html
  html = render_template(
    'templates/news_html.html',
    today="2023년 9월 7일",
    nickname="나는범인이다",
    news1_unlone="한국경제",
    news1_title="폭스바겐, 전기차 ID.3 부분변경 공개…국내출시 미정",
    news1_src="",
    news1_content="폭스바겐은 독일에서 전기차 ID.3의 부분변경 모델을 공개했다고 7일 밝혔다.ID.3는 2019년 9월 독일 프랑크푸르트 모터쇼에서 공개한 폭스바겐 ID 시리즈의 첫 번째 차량이다. 양산은 2020년 9월부터 시작했다.이번 모델은 2년6개월여 만에 이뤄지는 ID.3의 부분변경 모델이다. 폭스바겐은 지난해 국내에서 ID.4를 출시했다. ID.3는 국내 미출시 모델로, 이번 신형 ID.3 역시 국내 출시는 미정이다. 폭스바겐 New ID3신형 ID.3는 전면 범퍼와 공기 흡입구를 넓혔는데어쩔껀대그래서너가뭘할수있는데ㅋㅋ으이?너가코딩에대해알아몰알아챗지피티나써끼요오ㅗ소솟오오오송오",
    news1_picture="https://img.khan.co.kr/news/2021/08/23/l_2021082301002612800254111.webp",
    news2_unlone="NEWS1",
    news2_title="필수 동의 사라진다…'합리적 범위 내동의없이 개인정보 수집'(종합)",
    news2_src="",
    news2_content=" 개인정보보호법 개정안 국무회의 의결…9월15일 시행개인정보법 위반 과징금 상한액 매출 3억원 이하로 조정 고학수 개인정보보호위원회 위원장이 7일 오후 서울 종로구 세종대로 정부서울청사에서 개인정보 보호법 개정안 국무회의 심의·의결 관련 브리핑을 하고 있다. 2023.3.7/뉴스1 ⓒ News1 김명섭 기자  (서울=뉴스1) 윤수희 기자 = 앞으로 서비스 이용에 있어 필수적으로...",
    news2_picture="https://opgg-com-image.akamaized.net/attach/images/20200801183056.883339.jpg",
    news3_unlone="아시아경제",
    news3_title="'美, 브레이크 안밟으면 충돌' 中 외교부장의 작심비판(종합)",
    news3_src="",
    news3_content="대만문제 묻자 준비한 듯 헌법 꺼내 설명'전랑외교' 언급엔 '레토릭일 뿐' 친강 중국 외교부장이 압박 일변도의 대중국 정책을 고수하는 미국을 향해 '멈추지 않으면 재앙적 결과가 있을 것'이라고 강하게 경고했다. 부임 후 처음 진행된 기자회견이었지만 그는 시종일관 여유 있는 태도를 보이며 미국의 외교 노선을 작심 비판했다.친 부장은 7일 중국 베이징 미디어센터에서 개최된 내외신 기자회견에서 '만약 미국 측이 가드...'",
    news3_picture="https://image.ajunews.com/content/image/2021/06/17/20210617195546638372.jpg",
    etc_news1_unlone="한국경제",
    etc_news1_title="1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사1번째기사",
    etc_news1_src="https://www.naver.com",
    etc_news2_unlone="미국경제",
    etc_news2_title="2번째기사",
    etc_news2_src="https://www.naver.com",
    etc_news3_unlone="중국경제",
    etc_news3_title="3번째기사",
    etc_news3_src="",
    etc_news4_unlone="일본경제",
    etc_news4_title="4번째기사",
    etc_news4_src="",
    etc_news5_unlone="거울경제",
    etc_news5_title="5번째기사",
    etc_news5_src="https://www.naver.com",
  )
  
  news = MIMEText(html, "html")
  msg.attach(news)

  msg_list[idx] = msg

def send_email(user, msg):
  try:
      start = int(time.time())
      smtp_connect = connect_smtp_server()
      smtp_connect.sendmail(os.getenv('ADMIN_EMAIL'), user[1], msg.as_string())
      print("send user", str(user[0]),"'s run time(sec) :", int(time.time()) - start)
      smtp_connect.close()
    
  except Exception as e:
    logging.error("email send fail:"+str(e))