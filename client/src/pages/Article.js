import { useParams } from 'react-router-dom';
import AnalysisTextView from '../components/AnalysisTextView';
import FloatingButton from '../components/FloatingButton';
import SummaryTextView from '../components/SummaryTextView';
import './Article.css'
import { useState, useEffect } from 'react';
import { getArticleInfo } from '../Auth';

function Article() {

  let { articleID, companyID } = useParams();
  console.log(`${articleID} | ${companyID}`);

  const [article, setArticle] = useState({})

  useEffect(() => {
    getArticleInfo(articleID, companyID)
      .then((result) => {
        setArticle(result.data);
      });
  }, []);

  const text = "In the midst of bustling city life, where skyscrapers tower over bustling streets, there exists a hidden oasis of tranquility. Tucked away from the chaos, a small park blooms with vibrant colors and whispers of a gentle breeze. Here, time seems to slow down, inviting weary souls to rest upon the lush greenery and take solace in the song of chirping birds. As sunlight dances through the leaves, casting playful shadows upon the path, a sense of serenity envelops those who wander through this enchanting haven. It's a reminder that amidst the hustle and bustle, moments of peace and beauty can still be found, waiting to be discovered by those who seek them."
  
  /*
  const article = {
    title: "Tesla is in very big trouble",
    source: "BBC",
    companyID: "7",
    companyName: "Tesla",
    companyCode: "TSLA",
    date: "20/01/2024",
    summary: text,
    perception: 1,
    analysis: text,
    link: "TBD"
  }
  */

  const goToArticleLink = () => {
    console.log(article.link);
    window.open(article.link, "_blank");
  }

  return (
    <>
    <div id='article-pg'>
      <div id="pg-content">
        <div className='article-info narrow-content'>
            <h1>{article.title}</h1>
            <p>Source: {article.source}</p>
            <p>Company: <a href={`/company/${article.companyID}`} >{article.companyName} ({article.companyCode})</a></p>
            <p>Published: {article.date}</p>
        </div>

        <SummaryTextView title={"Summary"} text={article.summary} />

        <AnalysisTextView title={"Analysis"} perception={article.perception} text={article.analysis} />
      </div>

      <div id="fade-overlay" />

      {/* change action to visit website link */}
      <FloatingButton on={"Read full article"} off={""} isOn={true} action={goToArticleLink} />
    </div>
    </>
  );
}
  
export default Article;