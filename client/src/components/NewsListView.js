import "./NewsListView.css";

function NewsListView({ title }) {
  // view will also take news data as a parameter
  const data = [
    {
      id: 1,
      title: "Microsoft unveils new Windows 12 operating system",
      companyCode: "MSFT",
      author: "BBC",
      date: "20/02/2024",
      perception: 1
    },
    {
      id: 2,
      title: "Tesla's stock price hits all-time high",
      companyCode: "TSLA",
      author: "The Guardian",
      date: "18/02/2024",
      perception: 1
    },
    {
      id: 3,
      title: "Oracle is a really bad company",
      companyCode: "ORCL",
      author: "Sky",
      date: "27/01/2024",
      perception: 0
    },
    {
      id: 4,
      title: "Google announces expansion into new AI research lab",
      companyCode: "GOOGL",
      author: "BBC",
      date: "18/01/2024",
      perception: 2
    },
    {
      id: 5,
      title: "Amazon faces backlash over workplace conditions",
      companyCode: "AMZN",
      author: "The Independent",
      date: "10/01/2024",
      perception: 0
    }
  ];

  const perceptionToComponent = (p) => {
    if (p === 2) {
      return <p style={{ color: "var(--positive)" }}>Good</p>;
    } else if (p === 1) {
      return <p style={{ color: "var(--neutral)" }}>Neutral</p>;
    } else {
      return <p style={{ color: "var(--negative)" }}>Bad</p>;
    }
  };

  return (
    <>
      <div className="news-list-view">
        <h1>{title}</h1>
        <div className="list-section">
          {data.map((item) => (
            <div key={item.id} className="list-item">
              <div className="item-left">
                <p>{item.companyCode}</p>
              </div>
              <div className="item-text">
                <div className="text-top">
                  <p>{item.title}</p>
                </div>
                <div className="text-bottom">
                  <p>{item.author}</p>
                  <p>{item.date}</p>
                </div>                
              </div>
              <div className="item-right">
                <>{perceptionToComponent(item.perception)}</>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default NewsListView;
