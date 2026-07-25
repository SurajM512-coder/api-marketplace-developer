import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import BrowseApis from "./pages/BrowseApis";
import ApiDetails from "./pages/ApiDetails";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import OAuthSuccess from "./pages/OAuthSuccess";
import MySubscriptions from "./pages/MySubscriptions";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <main style={{ minHeight: "80vh", padding: "40px" }}>
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/login" element={<Login />} />

          <Route path="/register" element={<Register />} />

          <Route path="/oauth-success" element={<OAuthSuccess />} />

          <Route path="/apis" element={<BrowseApis />} />

          <Route path="/apis/:id" element={<ApiDetails />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/my-subscriptions"
            element={
              <ProtectedRoute>
                <MySubscriptions />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>

      <Footer />
    </BrowserRouter>
  );
}

export default App;