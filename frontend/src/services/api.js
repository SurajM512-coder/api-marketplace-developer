import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export const subscribeToApi = async (apiId) => {
  const response = await api.post(`/subscribe/${apiId}`);
  return response.data;
};

export const getMySubscriptions = async () => {
  const response = await api.get("/my-subscriptions");
  return response.data;
};

export const cancelSubscription = async (subscriptionId) => {
  const response = await api.delete(`/subscriptions/${subscriptionId}`);
  return response.data;
};

export default api;