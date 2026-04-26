import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/layout/Navbar";
import HomePage from "./pages/HomePage";
import Detection from "./pages/Detection";
import Dental from "./pages/Dental";

export default function App() {
  return (
    <Router>
      <Navbar />

      <div className="pt-20"> {/* spacing for fixed navbar */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/detection" element={<Detection />} />
          <Route path="/dental" element={<Dental />} />
        </Routes>
      </div>
    </Router>
  );
}