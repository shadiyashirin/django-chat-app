import { useEffect, useState } from "react";
import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Chat from "./chat";
import Login from "./Login";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("accessToken");
  return token ? children : <Navigate to="/login" />;
}

function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem("accessToken");
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route
          path="/chat"
          element={
            <PrivateRoute>
              <Chat token={token} roomId={6} />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<Navigate to="/chat" />} />
      </Routes>
    </Router>
  );
}

export default App;
