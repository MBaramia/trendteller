import "./NavMenu.css";
import { ReactComponent as HomeIcon } from "../images/home_icon_navmenu.svg";
import { ReactComponent as BrowseIcon } from "../images/browse_icon_navmenu.svg";
import { ReactComponent as NotificationsIcon } from "../images/bell_icon_white.svg";
import { ReactComponent as ProfileIcon } from "../images/profile_icon_navmenu.svg";
import { ReactComponent as TutorialIcon } from "../images/tutorial_icon_navmenu.svg";
import NavItem from "./NavItem";
import { processLogout } from "../Auth";

function NavMenu({ logOutUser }) {
  const handleLogout = async () => {
    const logOut = await processLogout();
    if (logOut.status) {
      logOutUser();
    } else {
      console.log(logOut.data);
    }
  };

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
          <button onClick={logOutUser} className="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </>
  );
}

export default NavMenu;
