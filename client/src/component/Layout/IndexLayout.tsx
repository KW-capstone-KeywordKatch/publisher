import { ReactNode } from "react";
import useVH from "react-viewport-height";
import IndexFooter from "../Index/IndexFooter/IndexFooter";
import GlobalNavigationBar from "../GlobalNavigationBar/GlobalNavigationBar";

interface IndexLayoutProps {
  children: ReactNode;
}

const IndexLayout: React.FunctionComponent<IndexLayoutProps> = ({
  children,
}) => {
  const vh = useVH();
  return (
    <div
      className="relative bg-white w-screen flex flex-col items-center justify-center"
      style={{
        height: 100 * vh,
      }}
    >
      <GlobalNavigationBar></GlobalNavigationBar>
      <div className="relative w-full h-full overflow-y-scroll bg-white drop-shadow-2xl flex flex-col items-center mt-[80px]">
        <div className="w-[1200px] grid grid-cols-1 gap-[20px]">{children}</div>
        <div className="w-full">
          <IndexFooter></IndexFooter>
        </div>
      </div>
    </div>
  );
};

export default IndexLayout;
