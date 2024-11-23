import './styles/App.css';
import AppRouter from "./components/AppRouter";
import {BrowserRouter} from "react-router-dom";
import Navbar from "./components/UI/Navbar/Navbar";
import {AuthContext} from "./context";
import {useEffect, useState} from "react";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [isLoading, setLoading] = useState(true);
    useEffect(() => {
        if(localStorage.getItem('auth')) {
            setIsAuth(true)
        }
        setLoading(false);
    }, [])


    return (
        <AuthContext.Provider value={{
            isAuth, setIsAuth, isLoading
        }}>
            <BrowserRouter>
                <Navbar/>
                <AppRouter/>
            </BrowserRouter>
        </AuthContext.Provider>


    )
}

export default App;
