import { userInfo } from "os";
import React, { useState } from "react";

const Index: React.FunctionComponent = () => {
  const [userInfos, setUserInfos] = useState<string[]>();

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

  const renderUserInfos = () => {
    if (userInfos) {
      return userInfos.map((userInfo) => {
        return <div className="border-2 rounded-sm p-[5px]">{userInfo}</div>;
      });
    } else {
      return <div>{"no user in there"}</div>;
    }
  };

  return (
    <div className="flex flex-col">
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
      <div></div>
    </div>
  );
};

export default Index;
