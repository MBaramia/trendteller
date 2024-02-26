import "./Header.css";
import HeaderLogo from "../images/header_logo.svg";
import ProfileIcon from "../images/profile_icon_header.svg";
import SearchBar from "./SearchBar";
import Bell from "./Bell";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header>
      <div className="left">
        <Link to="/">
          <img className="header-logo" src={HeaderLogo} alt="Trendteller logo" />
        </Link>
      </div>
      <div className="right">
        <div className="placeholder" />
        <SearchBar />
        <nav aria-label="header navigation">
          <Bell />

          <div id="profile-container">
            <Link to="/profile">
              <img class="profile-icon" src={ProfileIcon} alt="Profile icon" />
            </Link>
          </div>   

        </nav>
      </div>
    </header>
  );
}

export default Header;
