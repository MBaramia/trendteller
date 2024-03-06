import { useState, useEffect } from "react";
import CompanyListView from "../components/CompanyListView";
import NewsListView from "../components/NewsListView";
import RecommendedCompanyView from "../components/RecommendedCompanyView";
import { getFollowedCompanies, getAllNews, getRecommendedCompanies, processToggleFollowing } from "../Auth";
import io from "socket.io-client";

function Home() {
  const [hasLoaded, setHasLoaded] = useState(false);

  const [followedCompanies, setFollowedCompanies] = useState([]);
  const [news, setNews] = useState([]);
  const [recommendedCompanies, setRecommendedCompanies] = useState([])
  const [idToFollowing, setIdToFollowing] = useState({});

  useEffect(() => {
    fetchPageData();
    return setUpSocketListener();
  }, []);

  const fetchPageData = () => {
    let companies = []
    getFollowedCompanies()
      .then((result) => {
        setFollowedCompanies(result.data.data);
        companies = companies.concat(result.data.data)
        console.log("Companies: " + companies.length)
        return getAllNews();
      })
      .then((result) => {
        setNews(result.data.data);
        return getRecommendedCompanies();
      }).then((result) => {
        setRecommendedCompanies(result.data.data);
        companies = companies.concat(result.data.data)
        console.log("Companies: " + companies.length)
        setIdToFollowing(produceInitialAllFollowing(companies))
        setHasLoaded(true);
      });
  }

  const setUpSocketListener = () => {
    const socket = io("http://127.0.0.1:5000");
    socket.on("database_updated", (data) => {
      console.log(data);
      fetchPageData();
    });

    return () => socket.disconnect();
  }

  const produceInitialAllFollowing = (companies) => {
    let idToFollowing = {};
    for (const company of companies) {
      idToFollowing[company.id] = company.following;
    }
    return idToFollowing;
  };

  const toggleFollowing = (id) => {
    let newIdToFollowing = { ...idToFollowing };
    newIdToFollowing[id] = !idToFollowing[id];
    processToggleFollowing(id).then(() => {
      setIdToFollowing(newIdToFollowing);
    });
  };

  return (
    <>
      <div id="home-pg">
        <CompanyListView
          hasLoaded={hasLoaded}
          title={"Followed Companies"}
          data={followedCompanies}
          idToFollowing={idToFollowing}
          toggleFollowing={toggleFollowing}
        />
        <RecommendedCompanyView
          hasLoaded={hasLoaded}
          title={"Recommended For You"}
          data={recommendedCompanies}
          idToFollowing={idToFollowing}
          toggleFollowing={toggleFollowing}
        />
        <NewsListView hasLoaded={hasLoaded} title={"News"} data={news} />
        <div className="bottom-space"/>
      </div>
    </>
  );
}

export default Home;
