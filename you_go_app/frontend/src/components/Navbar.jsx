import React from 'react';
import { Link } from 'react-router-dom';
import NavItem from './NavItem'
function Navbar(props) {
    let active = props.active;
    return (
        <>
            <div className='fixed z-10 bottom-[2vh] w-full flex flex-col items-center justify-center'>
                <nav className=' text-white w-[95%] bg-white rounded-2xl shadow-md shadow-gray-200 p-4 flex flex-col items-center justify-center'>
                    <ul className='w-full flex flex-row items-center justify-evenly'>
                        <li><NavItem icon={'./src/assets/icons/home.svg'} content={'Home'} link={'/'} active={active == 'home'}/></li>
                        <li><NavItem icon={'./src/assets/icons/chat2.svg'} content={'Chat'} link={'/Chat'} active={active == 'chat'}/></li>
                        <li><NavItem icon={'./src/assets/icons/user.svg'} content={'Profile'} link={'/Profile'} active={active == 'profile'}/></li>
                        <li><NavItem icon={'./src/assets/icons/bill.svg'} content={'Billing'} link={'/Billing'} active={active == 'billing'}/></li>
                        <li><NavItem icon={'./src/assets/icons/location.svg'} content={'Tracking'} link={'/Tracking'} active={active == 'tracking'}/></li>
                    </ul>
                </nav>
            </div>
        </>
    );
} export default Navbar;