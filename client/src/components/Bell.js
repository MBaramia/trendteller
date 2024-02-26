import "./Bell.css";
import { ReactComponent as BellIcon } from "../images/bell_icon_header.svg";
import { Link } from "react-router-dom";

function Bell() {
  return (
    <div id="bell-container">
      <Link to="/notifications" className="bell-header">
        <p className="bell-text">5</p>
        <BellIcon className="bell-icon" />
      </Link>
    </div>
  );
}

export default Bell;