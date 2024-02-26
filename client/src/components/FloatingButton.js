import "./FloatingButton.css";

function FloatingButton({ on, off, isOn, action }) {

    return (

        <div id="floating-btn">
        <div onClick={action} className="btn">
            <p>{isOn? on : off}</p>
        </div>
        </div>

    );
}

export default FloatingButton;
