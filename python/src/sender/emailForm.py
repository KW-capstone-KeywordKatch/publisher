import smtplib
import os
from email.mime.image import MIMEImage
import src.sender.noPictureSrc as noPic
from flask import render_template
import logging
import time
from datetime import datetime

# 이메일 html 파츠 생성 ------------------------------------
def add_box_form(nickname):
  today = datetime.today()
  today_str = today.strftime("%Y년 %m월 %d일")

  html_logo_and_user_info_box = f'''
                  <!--로고 -->
                  <tr id="logo">
                    <td style="font-size: 24px; font-weight: 700">
                      KEYWORDKATCH
                    </td>
                  </tr>
                  <!--로고 밑 공백 -->
                  <tr id="space-between-logo-and-box">
                    <td style="padding: 7px"></td>
                  </tr>
                  <!--날짜와 닉네임 박스 -->
                  <tr id="box">
                    <td
                      align="center"
                      bgcolor="#000000"
                      style="padding: 40px 0 30px 0"
                    >
                      <p
                        style="color: white; font-size: 20px; font-weight: 700"
                      >
                        {today_str},<br />
                        {nickname}님에게 전달할 뉴스
                      </p>
                    </td>
                  </tr>
                  <!--박스 밑 공백 -->
                  <tr id="space">
                    <td style="padding: 10px"></td>
                  </tr>
  '''
  return html_logo_and_user_info_box

def add_main_article(keyword, article_info:list):

  article_title = article_info[3][0:30] + "..." if len(article_info[3]) > 30 else article_info[3]
  article_content = article_info[4][0:75] + "..." if len(article_info[4]) > 75 else article_info[4]
  article_picture_src = article_info[5] if article_info[5] != None else noPic.no_picture_src
  html_article_main = f'''
                  <tr id="keyword">
                    <td
                      align="center"
                      bgcolor="#000000"
                      style="padding: 10px 0 10px 0"
                    >
                      <p
                        style="color: white; font-size: 20px; font-weight: 700"
                      >
                        {keyword}와 관련된 뉴스
                      </p>
                    </td>
                  </tr>
                  <!--공백 -->
                  <tr>
                    <td style="padding: 10px"></td>
                  </tr>
                  <!--뉴스1 -->
                  <tr id="news1">
                    <td>
                      <table cellpadding="0" cellspacing="0">
                        <tr>
                          <td width="328" valign="top">
                            <table>
                              <tr>
                                <!-- 언론사 이름 -->
                                <td width="328" style="font-size: 14px">
                                  {article_info[2]}
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <table>
                                    <tr>
                                      <td width="328">
                                        <!-- 기사 주소 -->
                                        <a
                                          href="{article_info[6]}"
                                          style="
                                            font-size: 14px;
                                            font-weight: 700;
                                            text-decoration: none;
                                            color: #000000;
                                          "
                                        >
                                        <!--기사 제목-->
                                          {article_title}</a
                                        >
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>
                                        <table border="1" width="328"></table>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td style="padding: 7px"></td>
                                    </tr>
                                    <tr>
                                      <!-- 기사 내용 : 2줄 미만 -->
                                      <td width="328" style="font-size: 12px">
                                        {article_content}
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                          <td style="font-size: 0; line-height: 0" width="20">
                            &nbsp;
                          </td>
                          <td width="212">
                            <!-- 기사 사진-->
                            <img
                              style="width: 212px; height: 141px"
                              src="{article_picture_src}"
                              alt="기사사진"
                            />
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <!--뉴스 사이 공백 -->
                  <tr>
                    <td style="padding: 10px"></td>
                  </tr>
  '''
  return html_article_main

def add_sub_article(article_info_list:list):

  article_info_list = article_info_list[1:4] if len(article_info_list) >3 else article_info_list

  html_sub_articles = f'''
                    <!-- 텍스트 -->
                    <tr id="etc_news">
                      <td style="font-weight: 700">그 외 기사들</td>
                    </tr>
                    <!-- 텍스트 밑 공백 -->
                    <tr>
                      <td style="padding: 5px"></td>
                    </tr>
  '''

  for article_info in article_info_list:
    html_sub_article = f'''
                    <!--그 외 기사 1 -->
                    <tr id="etc_news1">
                      <td>
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td width="444" valign="top">
                              <table>
                                <tr>
                                  <!--언론사 이름-->
                                  <td width="444" style="font-size: 14px">
                                    {article_info[2]}
                                  </td>
                                </tr>
                                <tr>
                                  <!-- 기사 제목 -->
                                  <td width="444" style="font-size: 14px">
                                    {article_info[3]}
                                  </td>
                                </tr>
                              </table>
                            </td>
                            <td style="font-size: 0; line-height: 0" width="20">
                              &nbsp;
                            </td>
                            <td
                              width="96"
                              style="font-size: 14px; background-color: #000000"
                              align="center"
                            >
                              <!-- 기사 주소 -->
                              <a
                                width="100%"
                                href="{article_info[6]}"
                                style="text-decoration: none; color: white"
                              >
                                바로가기
                              </a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <!--그 외 기사 사이 공백 -->
                    <tr>
                      <td style="padding: 5px"></td>
                    </tr>
    '''
    html_sub_articles = html_sub_articles + html_sub_article

  return html_sub_articles

def add_html_start():
  html_start = '''
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
      <title>Demystifying Email Design</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    </head>
    <body style="margin: 0; padding: 0">
      <table cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td align="center">
            <!--배경 테두리 -->
            <table border="1" cellpadding="0" cellspacing="0" width="600">
              <tr>
                <td>
                  <table
                    align="center"
                    cellpadding="0"
                    cellspacing="0"
                    style="padding: 20px"
                  >

  '''
  return html_start

def add_html_end():
  html_end = '''

                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
  </html>
  '''
  return html_end
# 이메일 html 폼 동적 생성 -------------------------------------

def create_form(nickname, article_dict):
  # keyword 당 1개의 main 기사와 3개의 sub 기사 전달
  # keyword 당 무조건 1개 이상의 기사가 존재. 기사 없는 키워드는 여기까지 못 옴
  html_start = add_html_start()

  html_end = add_html_end()

  html_logo_and_user_info_box = add_box_form(nickname)

  html_article = ""

  for keyword, article_info_list in article_dict.items():
    html_main_article = add_main_article(keyword, article_info_list[0])
    if len(article_info_list) > 1 :
      html_sub_article = add_sub_article(article_info_list[1:])
      html_article = html_article + html_main_article + html_sub_article
    else :
      html_article = html_article + html_main_article

  return html_start + html_logo_and_user_info_box + html_article + html_end
