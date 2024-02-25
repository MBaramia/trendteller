import "./NavMenu.css";
import { ReactComponent as BellIcon } from "../images/bell_icon_header.svg";
import { Link } from "react-router-dom";

function NavMenu() {
  return (
    <>
      <div className="nav-menu">
        <div className="list-section">
          <ul>
            <li>
              <Link className="nav-link" to="/">
                <p>Home</p>
                <BellIcon className="icon" />
              </Link>
            </li>
            <li>
              <Link className="nav-link" to="/browse">
                <p>Browse</p>
                <BellIcon className="icon" />
              </Link>
            </li>
            <li>
              <Link className="nav-link" to="/notifications">
                <p>Notifications</p>
                <BellIcon className="icon" />
              </Link>
            </li>
          </ul>

          <ul>
            <li>
              <Link className="nav-link" to="/profile">
                <p>Profile</p>
                <BellIcon className="icon" />
              </Link>
            </li>
            <li>
              <Link className="nav-link" to="/tutorial">
                <p>Tutorial</p>
                <BellIcon className="icon" />
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <button>Logout</button>
        </div>
      </div>
    </>
  );
}

export default NavMenu;
