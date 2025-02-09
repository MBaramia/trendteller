import "./Bell.css";
import { ReactComponent as RingingBell } from "../images/bell_icon_header.svg";
import { ReactComponent as StillBell } from "../images/bell_icon_white.svg";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { getNoOfNotifications, setUpSocketListener } from "../Auth";

function Bell() {
  let [num, setNum] = useState(0);

  useEffect(() => {
    fetchPageData();
    return setUpSocketListener(fetchPageData);
  }, []);

  const fetchPageData = () => {
    getNoOfNotifications()
    .then((result) => {
      setNum(result.data);
    });
  }

  return (
    <div id="bell-container">
      <Link to="/notifications" className="bell-header">
        <p className={"bell-text" + (num === 0 ? " white" : "")}>{num}</p>
        {num === 0 ? <StillBell className="bell-icon" /> : <RingingBell className="bell-icon" />}
      </Link>
    </div>
  );
}

export default Bell;