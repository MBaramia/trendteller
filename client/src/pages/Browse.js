import RecommendedCompanyView from "../components/RecommendedCompanyView";
import CompanyListView from "../components/CompanyListView";
import { useState, useEffect } from "react";
import { getAllCompanies, getRecommendedCompanies, processToggleFollowing } from "../Auth";
import io from "socket.io-client";
// import './Browse.css'

function Browse() {
  const [hasLoaded, setHasLoaded] = useState(false);

  const [allCompanies, setAllCompanies] = useState([])
  const [recommendedCompanies, setRecommendedCompanies] = useState([])
  const [idToFollowing, setIdToFollowing] = useState({});

  useEffect(() => {
    fetchPageData();
    return setUpSocketListener();
  }, []);

  const fetchPageData = () => {
    getAllCompanies()
      .then((result) => {
        setAllCompanies(result.data.data);
        setIdToFollowing(produceInitialAllFollowing(result.data.data));
        return getRecommendedCompanies();
      }).then((result) => {
        setRecommendedCompanies(result.data.data);
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
      <div id="browse-pg">
        <RecommendedCompanyView
          hasLoaded={hasLoaded}
          title={"Recommended For You"}
          data={recommendedCompanies}
          idToFollowing={idToFollowing}
          toggleFollowing={toggleFollowing}
        />
        <CompanyListView
          hasLoaded={hasLoaded}
          title={"All Companies"}
          data={allCompanies}
          idToFollowing={idToFollowing}
          toggleFollowing={toggleFollowing}
        />
        <div className="bottom-space"/>
      </div>
    </>
  );
}

export default Browse;
