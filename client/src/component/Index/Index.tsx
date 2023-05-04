import { userInfo } from "os";
import React, { useState } from "react";

const Index: React.FunctionComponent = () => {
  const [userInfos, setUserInfos] = useState<string[]>();
  const [resultToSend, setResult] = useState<boolean>();

  const getUserInfo = () => {
    fetch("/get/user")
      .then((res) => res.json())
      .then((datas: JSON[]) => {
        const jsonToStringArray: string[] = datas.map((data) => {
          return data.toString();
        });
        setUserInfos(jsonToStringArray);
      });
  };

  const sendEmail = () => {
    fetch("/send").then(() => setResult(true));
  };

  const renderUserInfos = () => {
    if (userInfos) {
      return userInfos.map((userInfo) => {
        return <div className="border-2 rounded-sm p-[5px]">{userInfo}</div>;
      });
    } else {
      return <div>{"no user in there"}</div>;
    }
  };

  const connectUserRDS = () => {
    fetch("/connect/user").then(() => console.log("user RDS connect success!"));
  };

  const connectEditorRDS = () => {
    fetch("/connect/editor").then(() =>
      console.log("editor RDS connect success!")
    );
  };

  return (
    <div className="flex flex-col">
      <div className="flex flex-col mx-[30px] my-[20px]">
        <button
          className="border-2 rounded-sm p-[5px]"
          onClick={() => {
            connectUserRDS();
          }}
        >
          user rds 연결
        </button>
        <button
          className="border-2 rounded-sm p-[5px]"
          onClick={() => {
            connectEditorRDS();
          }}
        >
          editor rds 연결
        </button>
        <div className="flex flex-col">{renderUserInfos()}</div>
      </div>
      <div className="flex flex-col mx-[30px] my-[20px]">
        <button
          className="border-2 rounded-sm p-[5px]"
          onClick={() => {
            getUserInfo();
          }}
        >
          유저 리스트 보기
        </button>
        <div className="flex flex-col">{renderUserInfos()}</div>
      </div>
      <div className="flex flex-col mx-[30px] my-[20px]">
        <button
          className="border-2 rounded-sm p-[5px]"
          onClick={() => {
            sendEmail();
          }}
        >
          이메일 전송하기
        </button>
        {resultToSend && <div className="flex flex-col">{"send success"}</div>}
      </div>
    </div>
  );
};

export default Index;
