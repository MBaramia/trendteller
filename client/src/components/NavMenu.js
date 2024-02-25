import "./NavMenu.css";
import { ReactComponent as BellIcon } from "../images/bell_icon_header.svg";

function NavMenu() {

  return (
    <>
      <div className="nav-menu">
        <div className="list-section">
          <ul>
            <li><p>Home</p><BellIcon className="icon" /></li>
            <li><p>Browse</p><BellIcon className="icon" /></li>
            <li><p>Notifications</p><BellIcon className="icon" /></li>
          </ul>

          <ul>
            <li><p>Profile</p><BellIcon className="icon" /></li>
            <li><p>Tutorial</p><BellIcon className="icon" /></li>
          </ul>
        </div>

        <div><p>Logout</p></div>
      </div>
    </>
  );
}

export default NavMenu;
