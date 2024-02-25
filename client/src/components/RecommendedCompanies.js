import "./RecommendedCompanies.css";
import { ReactComponent as SmileyGood } from "../images/smiley_good_white.svg";
import { ReactComponent as SmileyNeutral} from "../images/smiley_neutral_white.svg";
import { ReactComponent as SmileyBad } from "../images/smiley_bad_white.svg";


function RecommendedCompanies({ title }) {
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
      perception: 1,
      following: false,
    }
  ];

  const perceptionToString = (p) => {
    if (p === 2) {
      return "Good";
    } else if (p === 1) {
      return "Neutral";
    } else {
      return "Bad";
    }
  };

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


  // style={{backgroundImage: 'linear-gradient(to bottom, ' + perceptionToBgColour(item.perception) + ', var(--dark-txt))' }}

  return (
    <>
      <div className="recommended-company-view">
        <h1>{title}</h1>
        <div className="grid-section">
          {data.map((item) => (
            <div key={item.id} className="grid-item">
              <div 
                style={{
                  backgroundImage: 'linear-gradient(to bottom, ' + 
                  perceptionToBgColour(item.perception) + 
                  ', var(--dark-txt))' 
                }} 
                className="item-text">
                <p>{item.code}</p>
                <p>{item.name}</p>
                <h3>{perceptionToSmiley(item.perception)}</h3>
                <p>£{item.price}</p>
                <p>{item.change}</p>
              </div>
              <div className="item-btn"><p>Follow</p></div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default RecommendedCompanies;
