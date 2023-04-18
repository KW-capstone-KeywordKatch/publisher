import { useNavigate } from "react-router-dom";
import LogoSvg from "../Icon/Svg/LogoSvg";
import MenuSvg from "../Icon/Svg/MenuSvg";

const GlobalNavigationBar: React.FunctionComponent = () => {
  const navigate = useNavigate();

  return (
    <div
      className="fixed top-0 w-full flex justify-center"
      style={{ boxShadow: "0px 4px 10px 2px rgba(0, 0, 0, 0.25)" }}
    >
      <div className="w-[1200px] h-[80px] flex items-center relative">
        <LogoSvg
          className="absolute left-0 cursor-pointer"
          onClick={() => {
            navigate("/");
          }}
        ></LogoSvg>
        <div className="absolute right-0 flex flex-row gap-[20px] justify-items-center items-center">
          <p className="cursor-pointer">SIGN IN</p>
          <p className="cursor-pointer">SIGN UP</p>
          <p className="cursor-pointer">CONTRACT</p>
          <MenuSvg></MenuSvg>
        </div>
      </div>
    </div>
  );
};

export default GlobalNavigationBar;
