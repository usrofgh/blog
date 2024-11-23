import React, {useContext} from 'react';
import {Route, Routes} from "react-router-dom";
import {privateRoutes, publicRoutes} from "../routes";
import {AuthContext} from "../context";
import Loader from "./UI/Loader/Loader";

const AppRouter = () => {
    const {isAuth, isLoading} = useContext(AuthContext)

    if (isLoading) {
        return <Loader/>
    }
    return (
        isAuth
            ?
            <Routes>
                {
                    privateRoutes.map(route => {
                        return (
                            <Route
                                key={route.path} // It's a good practice to add a key for each route
                                element={route.element}
                                path={route.path}
                                exact={route.exact}
                            />
                        );
                    })
                }
            </Routes>
            :
            <Routes>  {
                publicRoutes.map(route => {
                    return (
                        <Route
                            key={route.path} // It's a good practice to add a key for each route
                            element={route.element}
                            path={route.path}
                            exact={route.exact}
                        />
                    );
                })
            }
            </Routes>
    );
};

export default AppRouter;
