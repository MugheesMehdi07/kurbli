import { Navbar } from "./UI/navbar";
import { Right } from "./pages/right";
import { LeftText } from "./pages/left";
import { Scorebadge } from "./UI/score_badge";
import { useState } from "react";
import { useKurbilScore } from "./componets/kurbilScore";

function App() {
  const [scoreBadgeVisible, setScoreBadgeVisible] = useState(false);
  const { kurbilScore, setKurbilScore } = useKurbilScore();

  const toggleScoreBadge = () => {
    setScoreBadgeVisible(!scoreBadgeVisible);
  };
  const hideScoreBadge = () => {
    setScoreBadgeVisible(false);
  };
  return (
    <>
      <div className={scoreBadgeVisible ? "bg-gray-300" : ""}>
        <Navbar />
        <div className="grid grid-cols-1 md:grid-cols-2">
          <LeftText
            toggleScoreBadge={toggleScoreBadge}
            setKurbilScore={setKurbilScore}
            kurbilScore={kurbilScore}
          />
          <Right />
        </div>
        {scoreBadgeVisible && (
          <div className="flex items-center justify-center absolute top-0 w-full h-full z-50">
            <Scorebadge handleClose={hideScoreBadge} score={kurbilScore} />
          </div>
        )}
      </div>
    </>
  );
}

export default App;
