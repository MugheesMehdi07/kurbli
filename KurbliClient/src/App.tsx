import { useEffect, useState } from "react";
import { useKurbilScore } from "./components/kurbilScore";
import { LeftText } from "./pages/left";
import { Right } from "./pages/right";
import { Navbar } from "./UI/navbar";
import { ScoreBadge } from "./UI/score_badge";

function App() {
  const [scoreBadgeVisible, setScoreBadgeVisible] = useState(false);
  const [valid_address, setValid_address] = useState(false);
  const { kurbilScore, setKurbilScore } = useKurbilScore();
  const [score, setScore] = useState(false);

  const toggleScoreBadge = () => {
    setScoreBadgeVisible((prev) => !prev);
  };
  const hideScoreBadge = () => {
    setScoreBadgeVisible(false);
  };

  useEffect(() => {
    if (scoreBadgeVisible) {
      // Add class to hide overflow
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  }, [scoreBadgeVisible]);

  return (
    <>
      {/* <div className={scoreBadgeVisible ? "bg-gray-300" : ""}> */}
      <div className="calss">
        <Navbar />
        <div className="grid grid-cols-1 md:grid-cols-2">
          <LeftText
            toggleScoreBadge={toggleScoreBadge}
            setKurbilScore={setKurbilScore}
            kurbilScore={kurbilScore}
            setValid_address={setValid_address}
            valid_address={valid_address}
            score={score}
            setScore={setScore}
          />
          <Right valid_address={valid_address} />
        </div>
        {scoreBadgeVisible && (
          <div className="w-full h-full flex items-center justify-center fixed top-0 left-0 overflow-x-hidden overflow-y-auto z-50 bg-black bg-opacity-40">
            <ScoreBadge handleClose={hideScoreBadge} score={kurbilScore} />
          </div>
        )}
      </div>
    </>
  );
}

export default App;
