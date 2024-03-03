import { useState, useEffect } from "react";
import CompanyListView from "../components/CompanyListView";
import NewsListView from "../components/NewsListView";
import RecommendedCompanyView from "../components/RecommendedCompanyView";
import { getFollowedCompanies, getAllNews } from "../Auth";
// import './Home.css'

function Home() {
  const [followedCompanies, setFollowedCompanies] = useState([]);
  const [news, setNews] = useState([]);

  useEffect(() => {
    getFollowedCompanies()
      .then((result) => {
        setFollowedCompanies(result.data.data);
        setIdToFollowing(produceInitialAllFollowing());
        return getAllNews();
      })
      .then((result) => {
        setNews(result.data.data);
      });
  }, []);

  /*
  const followedCompanies = [
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

  */

  const recommendedCompanies = [
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
  ];

  /*
  const news = [
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
  ];
  */

  const produceInitialAllFollowing = () => {
    let idToFollowing = {};
    for (const company of followedCompanies) {
      idToFollowing[company.id] = company.following;
    }
    for (const company of recommendedCompanies) {
      idToFollowing[company.id] = company.following;
    }
    return idToFollowing;
  };

  let [idToFollowing, setIdToFollowing] = useState(produceInitialAllFollowing);

  const toggleFollowing = (id) => {
    let newIdToFollowing = { ...idToFollowing };
    newIdToFollowing[id] = !idToFollowing[id];
    setIdToFollowing(newIdToFollowing);
    // console.log(idToFollowing);
    // make server request
  };

  return (
    <>
      <div id="home-pg">
        <CompanyListView
          title={"Followed Companies"}
          data={followedCompanies}
          idToFollowing={idToFollowing}
          toggleFollowing={toggleFollowing}
        />
        <RecommendedCompanyView
          title={"Recommended For You"}
          data={recommendedCompanies}
          idToFollowing={idToFollowing}
          toggleFollowing={toggleFollowing}
        />
        <NewsListView title={"News"} data={news} />
      </div>
    </>
  );
}

export default Home;
