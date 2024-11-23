import About from "./pages/About";
import PostId from "./pages/PostId";
import Posts from "./pages/Posts";
import React from "react";
import Login from "./pages/Login";
import {Navigate} from "react-router-dom";

export const privateRoutes = [
    {path: '/about', element: <About/>, exact: true},
    {path: '/posts', element: <Posts/>, exact: true},
    {path: '/posts/:id', element: <PostId/> , exact: true},
    {path: '*', element: <Navigate to="/" replace/>, exact: true},
]


export const publicRoutes = [
    {path: '/login', element: <Login/>, exact: true},
    {path: '*', element: <Navigate to="/login" replace/>, exact: true},
]