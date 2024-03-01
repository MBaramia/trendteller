import "./NavItem.css";
import { Link, useLocation } from "react-router-dom";
import React from "react";

function NavItem({ navIcon, url, children }) {
  const { pathname } = useLocation();
  // console.log(pathname);
  const url_match = url === pathname;
  navIcon = React.cloneElement(navIcon, {
    className: "nav-icon",
    fill: url_match ? "var(--light-txt)" : "var(--nav-unselected)",
  });

  return (
    <Link className="nav-link" to={url}>
      <p className={url_match ? "selected-link link-text" : "link-text"}>
        {children}
      </p>
      {navIcon}
    </Link>
  );
}

export default NavItem;
