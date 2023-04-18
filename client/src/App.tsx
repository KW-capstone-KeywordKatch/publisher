import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";

const App: React.FunctionComponent = () => {
  const IndexPage = lazy(() => import("./page/IndexPage"));
  return (
    <Suspense fallback={<>로딩중...</>}>
      <Routes>
        <Route path="/" element={<IndexPage />} />
      </Routes>
    </Suspense>
  );
};

export default App;
