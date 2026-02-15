import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// Attach access token automatically
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto refresh on 401
API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refreshToken");

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/token/refresh/",
          { refresh: refreshToken }
        );

        const newAccessToken = response.data.access;
        localStorage.setItem("accessToken", newAccessToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return API(originalRequest);
      } catch (err) {
        logout();
      }
    }

    return Promise.reject(error);
  }
);

export const logout = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  window.location.href = "/";
};

export default API;
