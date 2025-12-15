import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// project imports
import Index from "./pages/Index/Index";
import LearningTree from "./pages/LearningTree/LearningTree";
import Stage from "./pages/Stage/Stage";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/LearningTree" element={<LearningTree />} />
        <Route path="/Stage" element={<Stage />} />
      </Routes>
    </Router>
  );
}

export default App
