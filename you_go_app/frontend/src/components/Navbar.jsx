import React from 'react';
import { Link } from 'react-router-dom';
function Navbar() {
    return (
        <nav className='bg-gray-800 text-white p-4'>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/Chat">Chat</a></li>
                <li><a href="/Profile">Profile</a></li>
                <li><a href="/Billing">Billing</a></li>
                <li><a href="/PublishOffer">Publish Offer</a></li>
                <li><a href="/PublishRequest">Publish Request</a></li>
                <li><a href="/SearchRides">Search Rides</a></li>
                <li><a href="/Support">Support</a></li>
                <li><a href="/Tracking">Tracking</a></li>
                <li><a href="/RoleChoice">Role Choice</a></li>
            </ul>
        </nav>
    );
} export default Navbar;