import "./NavItem.css";
import { Link } from "react-router-dom";

function NavItem({ navIcon, url , children }) {
  return (
    <Link className="nav-link" to={url}>
      <p>{children}</p>
      {navIcon}
    </Link>
  );
}

export default NavItem;