import { Navbar } from "./componets/navbar";
import { Right } from "./pages/right";
import { LeftText } from "./pages/left";
function App() {
  return (
    <>
      <div>
        <Navbar />
        <div className="grid grid-cols-1 md:grid-cols-2">
          <LeftText />
          <Right />
        </div>
      </div>
    </>
  );
}

export default App;
