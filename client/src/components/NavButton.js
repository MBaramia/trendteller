import "./NavButton.css";
import { ReactComponent as NavButtonIcon } from "../images/chevron_right_white.svg";

function NavButton({ navHidden, setNavHidden }) {

  const toggleNavHidden = () => {
    setNavHidden(!navHidden);
    console.log(navHidden);
  }

  return (
    <>
      <div onClick={toggleNavHidden} id="nav-btn" className={navHidden ? "" : "right"}>
        <NavButtonIcon />
      </div>
    </>
  );
}

export default NavButton;