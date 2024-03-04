import "./FloatingButton.css";
import Loading from "./Loading";

function FloatingButton({ hasLoaded, on, off, isOn, action }) {

    return (

        <div id="floating-btn">
            {hasLoaded ? <>
            <div onClick={action} className="btn">
                <p>{isOn? on : off}</p>
            </div>
            </>:<>
            <Loading />
            </>}
        </div>

    );
}

export default FloatingButton;
