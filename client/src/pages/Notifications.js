import { useState, useEffect } from "react";
import NewsListView from "../components/NewsListView";
import { getNotifications } from "../Auth";
// import './Notifications.css'

function Notifications() {
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    getNotifications()
      .then((result) => {
        setNotifications(result.data.data);
      });
  }, []);

  /*
  const notifications = [
    {
      id: 1,
      title: "Microsoft unveils new Windows 12 operating system",
      companyID: 7,
      companyCode: "MSFT",
      source: "BBC",
      date: "20/02/2024",
      perception: 1,
    },
    {
      id: 2,
      title: "Tesla's stock price hits all-time high",
      companyID: 20,
      companyCode: "TSLA",
      source: "The Guardian",
      date: "18/02/2024",
      perception: 1,
    },
    {
      id: 3,
      title: "Oracle is a really bad company",
      companyID: 12,
      companyCode: "ORCL",
      source: "Sky",
      date: "27/01/2024",
      perception: 0,
    },
    {
      id: 4,
      title: "Google announces expansion into new AI research lab",
      companyID: 9,
      companyCode: "GOOGL",
      source: "BBC",
      date: "18/01/2024",
      perception: 2,
    },
    {
      id: 5,
      title: "Amazon faces backlash over workplace conditions",
      companyID: 5,
      companyCode: "AMZN",
      source: "The Independent",
      date: "10/01/2024",
      perception: 0,
    },
    {
      id: 6,
      title: "Apple's new iPhone exceeds sales expectations",
      companyID: 3,
      companyCode: "AAPL",
      source: "CNBC",
      date: "25/02/2024",
      perception: 1,
    },
    {
      id: 7,
      title: "Facebook announces acquisition of popular messaging app",
      companyID: 8,
      companyCode: "FB",
      source: "TechCrunch",
      date: "22/02/2024",
      perception: 1,
    },
    {
      id: 8,
      title: "Netflix introduces new feature for personalized recommendations",
      companyID: 6,
      companyCode: "NFLX",
      source: "Reuters",
      date: "16/02/2024",
      perception: 1,
    },
    {
      id: 9,
      title: "IBM launches new quantum computing breakthrough",
      companyID: 11,
      companyCode: "IBM",
      source: "Financial Times",
      date: "12/02/2024",
      perception: 2,
    },
    {
      id: 10,
      title: "SpaceX successfully launches new satellite into orbit",
      companyID: 10,
      companyCode: "SPCE",
      source: "SpaceX News",
      date: "05/02/2024",
      perception: 1,
    },
  ];
  */

  return (
    <>
      <div id="notifications-pg">
        <NewsListView title={"Notifications"} data={notifications} />
      </div>
    </>
  );
}

export default Notifications;
