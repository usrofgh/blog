import React, {useContext} from 'react';
import {Link} from "react-router-dom";
import Mybutton from "../button/Mybutton";
import {AuthContext} from "../../../context";

const Navbar = () => {
    const {isAuth, setIsAuth} = useContext(AuthContext)

    const logout = () => {
        setIsAuth(false);
        localStorage.removeItem("auth");
    }
    return (
        <div className="navbar">
            <Mybutton onClick={logout}>Log out</Mybutton>
            <div className="navbar__links">
                <Link to="/about">About</Link>
                <Link to="/posts">Posts</Link>
            </div>
        </div>
    );
};

export default Navbar;
