CREATE TABLE user_interest (
  user_id INT NOT NULL,
  interest VARCHAR(255) NOT NULL,
  INDEX user_id_index (user_id)
);