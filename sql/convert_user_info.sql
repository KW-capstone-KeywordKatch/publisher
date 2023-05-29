-- 새로운 테이블 생성 및 데이터 이동
CREATE TABLE new_user_info (
  user_id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(255) NOT NULL UNIQUE,
  email_time VARCHAR(255),
  nickname VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);

INSERT INTO new_user_info (user_id, email, email_time, nickname, password)
SELECT user_id, email, email_time, nickname, password
FROM user_info;

DROP TABLE user_info;

-- 새로운 테이블 이름 변경
ALTER TABLE new_user_info RENAME TO user_info;
