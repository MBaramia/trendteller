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
        <img className="header-logo" src={HeaderLogo} alt="Trendteller logo" />
      </div>
      <div className="right">
        <div className="placeholder" />
        <SearchBar />
        <nav aria-label="header navigation">
          <Bell />
          <Link to="/">
            <img className="profile-icon" src={ProfileIcon} alt="Profile icon" />
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
