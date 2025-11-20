import { Route, Routes } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import Dashboard from "./pages/Dashboard";
import Scanner from "./pages/Scanner";

const App = () => {
  return (
    <div className="min-h-screen bg-midnight text-offWhite font-sans">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/scanner" element={<Scanner />} />
      </Routes>
      <Toaster position="bottom-right" />
    </div>
  );
};

export default App;

