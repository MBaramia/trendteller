import "./Header.css";
import HeaderLogo from "../images/header_logo.svg";
import ProfileIcon from "../images/profile_icon_header.svg";
import SearchBar from "./SearchBar";
import Bell from "./Bell";

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
          <a href="/">
            <img src={ProfileIcon} alt="Profile icon" />
          </a>
        </nav>
      </div>
    </header>
  );
}

export default Header;
