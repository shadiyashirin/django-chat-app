import { useState } from "react";
import API from "./api";

function Login({ setToken }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await API.post("token/", {
        username,
        password,
      });

      const data = response.data;


      localStorage.setItem("accessToken", data.access);
      localStorage.setItem("refreshToken", data.refresh);

      setToken(data.access);
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)} />

      <br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)} />

      <br />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;
