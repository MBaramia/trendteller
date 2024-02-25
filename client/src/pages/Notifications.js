import NewsListView from '../components/NewsListView';
// import './Notifications.css'

function Notifications() {

  const notifications = [
    {
      id: 1,
      title: "Microsoft unveils new Windows 12 operating system",
      companyID: 7,
      companyCode: "MSFT",
      author: "BBC",
      date: "20/02/2024",
      perception: 1
    },
    {
      id: 2,
      title: "Tesla's stock price hits all-time high",
      companyID: 20,
      companyCode: "TSLA",
      author: "The Guardian",
      date: "18/02/2024",
      perception: 1
    },
    {
      id: 3,
      title: "Oracle is a really bad company",
      companyID: 12,
      companyCode: "ORCL",
      author: "Sky",
      date: "27/01/2024",
      perception: 0
    },
    {
      id: 4,
      title: "Google announces expansion into new AI research lab",
      companyID: 9,
      companyCode: "GOOGL",
      author: "BBC",
      date: "18/01/2024",
      perception: 2
    },
    {
      id: 5,
      title: "Amazon faces backlash over workplace conditions",
      companyID: 5,
      companyCode: "AMZN",
      author: "The Independent",
      date: "10/01/2024",
      perception: 0
    }
  ];
  
  return (
    <>
    <div id='notifications-pg'>
      <NewsListView title={"Notifications"} data={notifications} />
    </div>
    </>
  );
}
  
export default Notifications;