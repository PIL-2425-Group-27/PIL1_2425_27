import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Profile from './pages/Profile';
import Billing from './pages/Billing';
import FAQ from './pages/FAQ';
import KYC from './pages/KYC';
import Login from './pages/Login';
import Register from './pages/Register';
import Notifications from './pages/Notifications';
import PublishOffer from './pages/PublishOffer';
import Settings from './pages/Settings';
import PublishRequest from './pages/PublishRequest';
import RideDetails from './pages/RideDetails';
import SearchRides from './pages/SearchRides';
import Support from './pages/Support';
import Tracking from './pages/Tracking';
import Landing from './pages/LandingPage';
import RoleChoice from './pages/RoleChoice';
import ForgotPassword from './pages/ForgotPassword';
import Verification from './pages/Verification';
import ChangePassword from './pages/ChangePassword';
import ModifProfile from './pages/ModifProfile';
import History from './pages/History';
import PasswordChanged from './pages/PasswordChanged';
import PrivateRoute from './utils/PrivateRoute';
import ChatSupportClient from './pages/ChatSupportClient';
import Chatbox from './components/Chatbox';
import ChatList from './components/ChatList';
import SearchChat from './pages/SearchChat';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Loading from './pages/Loading';


function App() {
  const [active, setActive] = useState(null); // null = loading
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("active_status");
    const parsed = JSON.parse(stored || "false"); // safely converts to boolean
    setActive(parsed);
  }, []);



  if (active === null) {
    return <Loading />; // or a spinner
  }

  return (
    <div className=''>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/Login" element={<Login />} />
          <Route path="/Register" element={<Register />} />
          <Route path="/ForgotPassword" element={<ForgotPassword />} />
          <Route path="/Verification" element={<Verification />} />
          <Route path="/PasswordChanged" element={<PasswordChanged />} />
          <Route path="/ChangePassword" element={<ChangePassword />} />

          {/* Private Routes */}
          <Route element={<PrivateRoute active={active} />}>
            <Route path="/" element={active ? <Home /> : <Landing />} />
            <Route path="/Chat" element={<Chat />} />
            <Route path="/Profile" element={<Profile />} />
            <Route path="/Billing" element={<Billing />} />
            <Route path="/FAQ" element={<FAQ />} />
            <Route path="/KYC" element={<KYC />} />
            <Route path="/Notifications" element={<Notifications />} />
            <Route path="/PublishOffer" element={<PublishOffer />} />
            <Route path="/Settings" element={<Settings />} />
            <Route path="/PublishRequest" element={<PublishRequest />} />
            <Route path="/RideDetails" element={<RideDetails />} />
            <Route path="/SearchRides" element={<SearchRides />} />
            <Route path="/Support" element={<Support />} />
            <Route path="/Tracking" element={<Tracking />} />
            <Route path="/RoleChoice" element={<RoleChoice />} />
            <Route path="/ModifProfile" element={<ModifProfile />} />
            <Route path="/History" element={<History />} />
            <Route path="/ChatSupportClient" element={<ChatSupportClient />} />
            <Route path="/ChatList" element={<ChatList />} />
            <Route path="/Chat/:chatId" element={<Chatbox />} />
            <Route path="/SearchChat" element={<SearchChat />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
