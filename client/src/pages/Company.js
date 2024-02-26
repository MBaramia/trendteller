import { useState } from 'react';
import AnalysisTextView from '../components/AnalysisTextView';
import FloatingButton from '../components/FloatingButton';
import SummaryTextView from '../components/SummaryTextView';
import './Company.css'
import { useParams } from 'react-router-dom';
import NewsListView from '../components/NewsListView';

function Company() {
  let { companyID } = useParams();
  console.log(companyID);

  const text = "In the midst of bustling city life, where skyscrapers tower over bustling streets, there exists a hidden oasis of tranquility. Tucked away from the chaos, a small park blooms with vibrant colors and whispers of a gentle breeze. Here, time seems to slow down, inviting weary souls to rest upon the lush greenery and take solace in the song of chirping birds. As sunlight dances through the leaves, casting playful shadows upon the path, a sense of serenity envelops those who wander through this enchanting haven. It's a reminder that amidst the hustle and bustle, moments of peace and beauty can still be found, waiting to be discovered by those who seek them."
  
  const company = {
    id: 5,
    code: "TSLA",
    name: "Tesla, Inc.",
    overview: text,
    perception: 0,
    analysis: text,
    following: true
  }

  const stockData = {
    price: 182,
    weekChangeNum: -23,
    weekChangePer: -13.8,
  }

  const news = [
    {
      id: 1,
      title: "Microsoft unveils new Windows 12 operating system",
      companyID: 20, 
      companyCode: "TSLA", 
      source: "BBC",
      date: "20/02/2024",
      perception: 1
    },
    {
      id: 2,
      title: "Tesla's stock price hits all-time high",
      companyID: 20,
      companyCode: "TSLA",
      source: "The Guardian",
      date: "18/02/2024",
      perception: 1
    },
    {
      id: 3,
      title: "Oracle is a really bad company",
      companyID: 20,
      companyCode: "TSLA",
      source: "Sky",
      date: "27/01/2024",
      perception: 0
    },
    {
      id: 4,
      title: "Google announces expansion into new AI research lab",
      companyID: 20,
      companyCode: "TSLA",
      source: "BBC",
      date: "18/01/2024",
      perception: 2
    },
    {
      id: 5,
      title: "Amazon faces backlash over workplace conditions",
      companyID: 20,
      companyCode: "TSLA",
      source: "The Independent",
      date: "10/01/2024",
      perception: 0
    }
  ];
  

  let [isFollowing, setIsFollowing] = useState(true);

  const toggleCompanyFollow = () => {
    setIsFollowing(!isFollowing);
  }

  const perceptionToComponent = (p) => {
    if (p === 2) {
      return <span style={{ color: "var(--positive)" }}>Good</span>;
    } else if (p === 1) {
      return <span style={{ color: "var(--neutral)" }}>Neutral</span>;
    } else {
      return <span style={{ color: "var(--negative)" }}>Bad</span>;
    }
  };

  return (
    <>
    <div id='company-pg'>
      <div id='pg-content'>
        <div className='chart-area'>
          <div className='company-info'>
            <div className='info-left'>
              <h1>{company.code}</h1>
              <h3>{company.name}</h3>
            </div>
            <div className='info-right'>
              <p>Stock price: £{stockData.price}</p>
              <p>{stockData.weekChangeNum > 0 ? "+" : "-"}£{Math.abs(stockData.weekChangeNum)} ({stockData.weekChangePer}%) from last week</p>
              <p>Public opinion: {perceptionToComponent(company.perception)}</p>
            </div>
          </div>

          <div id='chart'>

          </div>

        </div>

        <SummaryTextView title={"Overview"} text={company.overview} />

        <AnalysisTextView title={"Analysis"} perception={company.perception} text={company.analysis} />
        
        <NewsListView title={"Recent News"} data={news} />
      </div>

      <div id="fade-overlay" />

      <FloatingButton on={"Unfollow"} off={"Follow"} isOn={isFollowing} action={toggleCompanyFollow} />

    </div>
    
    </>
  );
}
  
export default Company;