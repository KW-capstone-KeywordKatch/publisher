interface MenuSvgProps {
  className?: string;
}

const MenuSvg: React.FunctionComponent<MenuSvgProps> = ({ className = "" }) => {
  return (
    <svg
      width="15"
      height="13"
      viewBox="0 0 15 13"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <line
        y1="1.20001"
        x2="15"
        y2="1.20001"
        stroke="#101010"
        stroke-width="2"
      />
      <line
        y1="6.40002"
        x2="15"
        y2="6.40002"
        stroke="#101010"
        stroke-width="2"
      />
      <line
        x1="7"
        y1="11.6"
        x2="15"
        y2="11.6"
        stroke="#101010"
        stroke-width="2"
      />
    </svg>
  );
};

export default MenuSvg;
