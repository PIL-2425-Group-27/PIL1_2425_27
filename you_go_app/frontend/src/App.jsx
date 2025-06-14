import { BrowserRouter, Routes, Route } from 'react-router-dom';
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
let active = true;
let page = active ? <Home /> : <Landing />
function App() {
  const isAuthenticated = false;
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/Login" element={<Login />} />
        <Route path="/Register" element={<Register />} />
        <Route path="/ForgotPassword" element={<ForgotPassword />} />
        <Route path="/Verification" element={<Verification />} />
        <Route path="/PasswordChanged" element={<PasswordChanged />} />
        <Route path="/ChangePassword" element={<ChangePassword />} />
        {/* Private routes */}
        <Route element={<PrivateRoute />}>
          <Route path="/" element={page} />
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
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App
