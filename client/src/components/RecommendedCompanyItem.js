import "./RecommendedCompanyView.css";
import { ReactComponent as SmileyGood } from "../images/smiley_good_white.svg";
import { ReactComponent as SmileyNeutral} from "../images/smiley_neutral_white.svg";
import { ReactComponent as SmileyBad } from "../images/smiley_bad_white.svg";
import { useState } from "react";

function RecommendedCompanyItem({ company }) {
  let [isFollowing, setIsFollowing] = useState(company.following);

  const goToCompanyPage = () => {
    // change eventually
    console.log(company.id);
  }

  const toggleFollow = (e) => {
    setIsFollowing(!isFollowing);
    e.stopPropagation();
  }

  const perceptionToBgColour = (p) => {
    if (p === 2) {
      return "var(--positive)";
    } else if (p === 1) {
      return "var(--neutral)";
    } else {
      return "var(--negative)";
    }
  }

  const perceptionToSmiley = (p) => {
    if (p === 2) {
      return <SmileyGood className="smiley" />;
    } else if (p === 1) {
      return <SmileyNeutral className="smiley" />;
    } else {
      return <SmileyBad className="smiley" />;
    }
  }

  const buttonText = (f) => {
    if (f) {
      return "Unfollow";
    } else {
      return "Follow";
    }
  }

  return (
    <>
      <div onClick={goToCompanyPage} className="grid-item">
        <div 
          style={{
            backgroundImage: 'linear-gradient(to bottom, ' + 
            perceptionToBgColour(company.perception) + 
            ', var(--dark-txt))' 
          }} 
          className="item-text">
          <p>{company.code}</p>
          <p>{company.name}</p>
          <h3>{perceptionToSmiley(company.perception)}</h3>
          <p>£{company.price}</p>
          <p>{company.change}</p>
        </div>
        <div className="item-btn" onClick={toggleFollow}><p>{buttonText(isFollowing)}</p></div>
      </div>
    </>
  );
}

export default RecommendedCompanyItem;
