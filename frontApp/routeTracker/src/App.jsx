import { BrowserRouter, Route, Routes } from "react-router-dom";
import DriverView from './DriverView';
import ChooseDriver from './ChooseDriver';
import Test from "./Test";
import Driving from "./Driving";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/test" element={<Test />} />
        <Route path="/driving" element={<Driving />} />
        <Route path="/driver" element={<DriverView />} />
        <Route path="/choose-driver" element={<ChooseDriver />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
