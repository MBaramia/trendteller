import "./AnalysisTextView.css";

function AnalysisTextView({ title, perception, text }) {

  const perceptionToComponent = (p) => {
    if (p === 2) {
      return <h3 style={{color: "var(--positive)"}}>Good</h3>;
    } else if (p === 1) {
      return <h3 style={{color: "var(--neutral)"}}>Neutral</h3>;
    } else {
      return <h3 style={{color: "var(--negative)"}}>Bad</h3>;
    }
  }

  return (
    <>
      <div className="analysis-text-view narrow-content">
        <h2>{title}</h2>
        <div className="text-analysis">
          <>{perceptionToComponent(perception)}</>
        </div>
        <div className="text-content">
          <p>{text}</p>
        </div>
      </div>
    </>
  );
}

export default AnalysisTextView;
