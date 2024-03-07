import { useState, useEffect } from "react";
import NewsListView from "../components/NewsListView";
import { getNotifications, setUpSocketListener } from "../Auth";

function Notifications() {
  const [hasLoaded, setHasLoaded] = useState(false);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    fetchPageData();
    return setUpSocketListener(fetchPageData);
  }, []);

  const fetchPageData = () => {
    getNotifications()
    .then((result) => {
      setNotifications(result.data.data);
      setHasLoaded(true);
    });
  }

  return (
    <>
      <div id="notifications-pg">
        <NewsListView hasLoaded={hasLoaded} title={"Notifications"} data={notifications} />
        <div className="bottom-space"/>
      </div>
    </>
  );
}

export default Notifications;
