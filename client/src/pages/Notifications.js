import { useState, useEffect } from "react";
import NewsListView from "../components/NewsListView";
import { getNotifications, setUpSocketListener } from "../Auth";

function Notifications() {
  const [hasLoaded, setHasLoaded] = useState(false);
  const [notifications, setNotifications] = useState(null);

  useEffect(() => {
    fetchPageData();
  }, []);

  useEffect(() => {
    if (notifications !== null) {
      return setUpSocketListener(fetchNewPageData);
    }
  }, [notifications]);

  const fetchPageData = () => {
    getNotifications()
    .then((result) => {
      setNotifications(result.data.data);
      setHasLoaded(true);
    });
  }

  const fetchNewPageData = () => {
    console.log("old page data: " + notifications)
    getNotifications()
    .then((result) => {
      setNotifications(notifications.concat(result.data.data));
    });
  }

  return (
    <>
      <div id="notifications-pg">
        <NewsListView hasLoaded={hasLoaded} title={"Notifications"} data={notifications ?? []} />
        <div className="bottom-space"/>
      </div>
    </>
  );
}

export default Notifications;
