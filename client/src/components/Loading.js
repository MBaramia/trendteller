import './Loading.css';
import { ReactComponent as LoadingIcon } from "../images/loading_icon.svg";

function Loading() {

  return (
    <>
      <div className="loading">
        <div className='loading-icon'>
          <LoadingIcon />
        </div>
      </div>
    </>
  );
}

export default Loading;
