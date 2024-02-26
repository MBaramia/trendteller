import "./NavMenu.css";
import { Link } from "react-router-dom";
import { ReactComponent as BellIcon } from "../images/bell_icon_header.svg";
import { ReactComponent as HomeIcon} from "../images/home_icon_navmenu.svg";
import { ReactComponent as BrowseIcon} from "../images/browse_icon_navmenu.svg";
import { ReactComponent as NotificationsIcon } from "../images/bell_icon_white.svg";
import { ReactComponent as ProfileIcon } from "../images/profile_icon_navmenu.svg";
import { ReactComponent as TutorialIcon } from "../images/tutorial_icon_navmenu.svg";

function NavMenu() {
  return (
    <>
      <div className="nav-menu">
        <div className="list-section">
          <ul>
            <li>
              <Link className="nav-link" to="/">
                <p>Home</p>
                <HomeIcon className="nav-icon" />
              </Link>
            </li>
            <li>
              <Link className="nav-link" to="/browse">
                <p>Browse</p>
                <BrowseIcon className="nav-icon" />
              </Link>
            </li>
            <li>
              <Link className="nav-link" to="/notifications">
                <p>Notifications</p>
                <NotificationsIcon className="nav-icon" />
              </Link>
            </li>
          </ul>

          <ul>
            <li>
              <Link className="nav-link" to="/profile">
                <p>Profile</p>
                <ProfileIcon className="nav-icon" />
              </Link>
            </li>
            <li>
              <Link className="nav-link" to="/tutorial">
                <p>Tutorial</p>
                <TutorialIcon className="nav-icon" />
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <button class="logout-btn">Logout</button>
        </div>
      </div>
    </>
  );
}

export default NavMenu;
