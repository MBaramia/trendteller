import { useState } from 'react';
import AnalysisTextView from '../components/AnalysisTextView';
import FloatingButton from '../components/FloatingButton';
import SummaryTextView from '../components/SummaryTextView';
import './Company.css'

function Company() {
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
      <div className='chart-area'>
        <div className='company-info'>
          <div className='info-left'>
            <h1>{company.code}</h1>
            <p>{company.name}</p>
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

      <FloatingButton on={"Unfollow"} off={"Follow"} isOn={isFollowing} action={toggleCompanyFollow} />
    </div>
    </>
  );
}
  
export default Company;