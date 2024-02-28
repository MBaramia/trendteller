import "./NavMenu.css";
import { ReactComponent as HomeIcon } from "../images/home_icon_navmenu.svg";
import { ReactComponent as BrowseIcon } from "../images/browse_icon_navmenu.svg";
import { ReactComponent as NotificationsIcon } from "../images/bell_icon_white.svg";
import { ReactComponent as ProfileIcon } from "../images/profile_icon_navmenu.svg";
import { ReactComponent as TutorialIcon } from "../images/tutorial_icon_navmenu.svg";
import NavItem from "./NavItem";

function NavMenu() {
  return (
    <>
      <div className="nav-menu">
        <div className="list-section">
          <ul>
            <li>
              <NavItem url="/" navIcon={<HomeIcon />}>
                Home
              </NavItem>
            </li>
            <li>
              <NavItem url="/browse" navIcon={<BrowseIcon />}>
                Browse
              </NavItem>
            </li>
            <li>
              <NavItem url="/notifications" navIcon={<NotificationsIcon />}>
                Notifications
              </NavItem>
            </li>
          </ul>

          <ul>
            <li>
              <NavItem url="/profile" navIcon={<ProfileIcon />}>
                Profile
              </NavItem>
            </li>
            <li>
              <NavItem url="/tutorial" navIcon={<TutorialIcon />}>
                Tutorial
              </NavItem>
            </li>
          </ul>
        </div>

        <div>
          <button className="logout-btn">Logout</button>
        </div>
      </div>
    </>
  );
}

export default NavMenu;
