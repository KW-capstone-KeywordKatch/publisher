import React, { useState } from "react";

interface ApiResponse {
  success : boolean,
  error : string,
  data : JSON;
}

interface Article {
    company : string,
    content : string,
    id : number,
    image : string | undefined,
    link : string,
    time : Date,
    title : string,
}

type ArticleDict = Record<string, Article[]>;

const Index: React.FunctionComponent = () => {
  const [userInfos, setUserInfos] = useState<string[]>();
  const [userId, setUserId] = useState<string>("");
  const [resultToSend, setResult] = useState<boolean>();
  const [resultToGet, setResult2] = useState<boolean>();
  const [resultData, setResultData] = useState<ApiResponse>();
  const [userArticleData, setUserArticleData] = useState<ArticleDict>({});

  // response인 dict를 convert해줌
  const convertToArticles = (data: Record<string, any>): Record<string, Article[]> => {
    const convertData: ArticleDict = {};
  
    for (const [key, value] of Object.entries(data)) {
      const articles: Article[] = Object.values(value).map((item: any) => ({
        company: item.company,
        content: item.content,
        id: item.id,
        image: item.image,
        link: item.link,
        time: new Date(item.time),
        title: item.title,
      }));
  
      convertData[key] = articles;
    }
  
    return convertData;
  }

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
    fetch("/send")
      .then((response)=> response.json())
      .then((responseData: ApiResponse) => {
        if(!responseData.success){
          return;
        }
        setResultData(responseData);
        setResult(true);
      });
  };

  // userArticleData 사용법 ------------------------------------------------------
  const sendGetUserArticles = () => {
    const URL = "/articles/"+userId.toString();

    fetch(URL)
    .then((response)=> response.json())
    .then((responseData) => {
      const convertData = convertToArticles(responseData);
      setUserArticleData(convertData);
      setResult2(true);
    });
  };

  const renderUserArticles = () => {
    return (
      <div>
        {userArticleData ? (
          Object.keys(userArticleData).map((key) => (
            <div key={key}>
              <div>{key}</div>
              {userArticleData[key].map((article) => (
                <div key={article.id}>
                  <div>{article.title}</div>
                  <div>{article.content}</div>
                  <div>{article.company}</div>
                </div>
              ))}
            </div>
          ))) : ( <p>Loading articles...</p>)
        }
      </div>
    );
  }

  const renderUserInfos = () => {
    if (userInfos) {
      return userInfos.map((userInfo) => {
        return <div className="border-2 rounded-sm p-[5px]">{userInfo}</div>;
      });
    } else {
      return <div>{"no user in there"}</div>;
    }
  };

  const connectLocalRDS = () => {
    fetch("/connect/local").then(() =>
      console.log("local RDS connect success!")
    );
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
            connectLocalRDS();
          }}
        >
          local rds 연결
        </button>
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
        {resultToSend && <div className="flex flex-col">{JSON.stringify(resultData)}</div>}
      </div>
      <div className="flex flex-col mx-[30px] my-[20px]">
        <input className="flex w-fit border-2" value={userId} onChange={(e)=>setUserId(e.target.value)}></input>
        <button
          className="border-2 rounded-sm p-[5px]"
          onClick={() => {
            sendGetUserArticles();
          }}
        >
          해당 사용자의 키워드와 관련된 기사 정보 받기
        </button>
        {resultToGet && <div className="flex flex-col">{
          renderUserArticles()
        }</div>}
      </div>
    </div>
  );
};

export default Index;
