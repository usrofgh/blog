import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";
import PostService from "../API/PostService";
import {useFetching} from "../hooks/useFetching";
import Loader from "../components/UI/Loader/Loader";

const PostId = () => {
    const params = useParams()
    const [post, setPost] = useState({});
    const [comments, setComments] = useState([]);
    const [fetchPostById, isLoading, error] = useFetching(async (id) => {
        const response = await PostService.getByID(id)
        setPost(response.data);
    })

    const [fetchComments, isCommLoading, comError] = useFetching(async (id) => {
        const response = await PostService.getCommentsByPostId(id)
        setComments(response.data);
    })
    useEffect(() => {
        fetchPostById(params.id)
        fetchComments(params.id)
    }, []);

    return (
        <div>

            {isLoading
                ? <div style={{display: 'flex', justifyContent: 'center', marginTop: 100}}><Loader/></div>
                : <div>
                    <h1>Post details of {params.id}</h1>
                    {post.id}. {post.title}
                </div>
            }
            {isLoading
                ? <div style={{display: 'flex', justifyContent: 'center', marginTop: 100}}><Loader/></div>
                : <div>
                    <h1 style={{marginTop: 200}}>Comments of {params.id}</h1>
                    <div>
                        {comments.map(comm =>
                            <div style={{marginTop: 15}}>
                                <h5>{comm.email}</h5>
                                <div>{comm.body}</div>
                            </div>
                        )}
                    </div>
                </div>
            }
        </div>
    );
};

export default PostId;
