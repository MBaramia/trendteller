import "./Bell.css";
import { ReactComponent as BellIcon } from "../images/bell_icon_header.svg";
import { Link } from "react-router-dom";

function Bell() {
  return (
    <Link to="/" className="bell-header">
      <p className="bell-text">5</p>
      <BellIcon />
    </Link>
  );
}

export default Bell;