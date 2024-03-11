import './Tutorial.css'
import SummaryTextView from '../components/SummaryTextView';
import Vimeo from '@u-wave/react-vimeo';

function Tutorial() {

  const transcript = "In the midst of bustling city life, where skyscrapers tower over bustling streets, there exists a hidden oasis of tranquility. Tucked away from the chaos, a small park blooms with vibrant colors and whispers of a gentle breeze. Here, time seems to slow down, inviting weary souls to rest upon the lush greenery and take solace in the song of chirping birds. As sunlight dances through the leaves, casting playful shadows upon the path, a sense of serenity envelops those who wander through this enchanting haven. It's a reminder that amidst the hustle and bustle, moments of peace and beauty can still be found, waiting to be discovered by those who seek them.";

  return (
    <>
    <div id='tutorial-pg'>
      <div className='video-area narrow-content'>
          <h2>Video</h2>

          <Vimeo
            video={921874448}
          />

      </div>
      <SummaryTextView hasLoaded={true} title={"Transcript"} text={transcript} />
    </div>
    </>
  );
}
  
export default Tutorial;