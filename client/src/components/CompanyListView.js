import "./CompanyListView.css";

function CompanyListView({ title }) {
  // view will also take company data as a parameter
  const data = [
    {
      id: 15,
      name: "Oracle",
      code: "ORCL",
      price: "82.49",
      change: "+9.3%",
      perception: 0,
      following: true,
    },
    {
      id: 7,
      name: "PayPal",
      code: "PYPL",
      price: "220.61",
      change: "-14.9%",
      perception: 2,
      following: true,
    },
    {
      id: 9,
      name: "Adobe",
      code: "ADBE",
      price: "632.24",
      change: "+21.3%",
      perception: 2,
      following: false,
    },
    {
      id: 10,
      name: "Intel",
      code: "INTC",
      price: "58.94",
      change: "+8.7%",
      perception: 0,
      following: true,
    },
    {
      id: 19,
      name: "Uber",
      code: "UBER",
      price: "46.93",
      change: "+7.9%",
      perception: 0,
      following: false,
    },
    {
      id: 12,
      name: "Twitter",
      code: "TWTR",
      price: "63.78",
      change: "-10.1%",
      perception: 0,
      following: true,
    },
    {
      id: 3,
      name: "Microsoft",
      code: "MSFT",
      price: "242.01",
      change: "-18.3%",
      perception: 1,
      following: true,
    },
    {
      id: 4,
      name: "Alphabet",
      code: "GOOGL",
      price: "2765.95",
      change: "+17.8%",
      perception: 1,
      following: false,
    },
    {
      id: 18,
      name: "Zoom",
      code: "ZM",
      price: "279.23",
      change: "+16.2%",
      perception: 0,
      following: true,
    },
    {
      id: 6,
      name: "NVIDIA",
      code: "NVDA",
      price: "651.52",
      change: "-28.4%",
      perception: 2,
      following: false,
    },
    {
      id: 1,
      name: "Apple",
      code: "AAPL",
      price: "143.71",
      change: "+12.5%",
      perception: 1,
      following: false,
    },
    {
      id: 14,
      name: "Salesforce",
      code: "CRM",
      price: "260.35",
      change: "-11.8%",
      perception: 0,
      following: true,
    },
    {
      id: 0,
      name: "Tesla",
      code: "TSLA",
      price: "134.53",
      change: "+23.7%",
      perception: 1,
      following: true,
    },
    {
      id: 11,
      name: "AMD",
      code: "AMD",
      price: "111.23",
      change: "+27.9%",
      perception: 0,
      following: false,
    },
    {
      id: 17,
      name: "Square",
      code: "SQ",
      price: "243.68",
      change: "+18.6%",
      perception: 0,
      following: true,
    },
    {
      id: 5,
      name: "Facebook",
      code: "FB",
      price: "323.19",
      change: "+20.6%",
      perception: 2,
      following: true,
    },
    {
      id: 16,
      name: "Shopify",
      code: "SHOP",
      price: "1244.86",
      change: "-32.5%",
      perception: 0,
      following: false,
    },
    {
      id: 13,
      name: "Cisco",
      code: "CSCO",
      price: "53.42",
      change: "+5.6%",
      perception: 0,
      following: false,
    },
    {
      id: 2,
      name: "Amazon",
      code: "AMZN",
      price: "3182.7",
      change: "-15.2%",
      perception: 1,
      following: true,
    },
    {
      id: 8,
      name: "Netflix",
      code: "NFLX",
      price: "602.36",
      change: "+25.7%",
      perception: 2,
      following: true,
    },
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
      <div className="company-list-view">
        <h1>{title}</h1>
        <div className="list-section">
          <div className="list-header">
            <p>Name</p>
            <p>Price</p>
            <p>Change</p>
            <p>Perception</p>
            <p>Following</p>
          </div>
          {data.map((item) => (
            <div key={item.id} className="list-row">
              <p>{item.name}</p>
              <p>£{item.price}</p>
              <p>{item.change}</p>
              <>{perceptionToComponent(item.perception)}</>
              <p>{item.following.toString()}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default CompanyListView;
