from sqladmin import ModelView

from src.back.models.comments import CommentModel as Comment
from src.back.models.posts import PostModel as Post
from src.back.models.users import UserModel as User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    page_size = 50

    can_create = True
    can_edit = True

    column_list = [
        User.id, User.email, User.auto_reply, User.auto_reply_sec_delay,
        User.is_activated, User.is_admin, User.registered_at,
        User.posts, User.comments
    ]
    column_details_list = column_list

    column_searchable_list = [User.email]

    form_columns = [
        User.email, User.password, User.auto_reply,
        User.auto_reply_sec_delay, User.is_activated, User.is_admin
    ]


class PostAdmin(ModelView, model=Post):
    name = "Post"
    name_plural = "Posts"
    icon = "fa-solid fa-star"
    page_size = 50

    can_create = True
    can_edit = True

    column_list = [
        Post.id, Post.content, Post.author, Post.is_blocked,
        Post.created_at, Post.updated_at
    ]
    column_details_list = column_list

    form_columns = [Post.content, Post.author_id, Post.is_blocked]


class CommentAdmin(ModelView, model=Comment):
    name = "Comment"
    name_plural = "Comments"
    icon = "fa-solid fa-comment"
    page_size = 50

    can_create = True
    can_edit = True

    column_list = [
        Comment.id, Comment.author, Comment.post,
        Comment.content, Comment.is_blocked, Comment.parent_comment_id,
        Comment.created_at, Comment.updated_at
    ]

    column_details_list = column_list

    form_columns = [Comment.author, Comment.post, Comment.content, Comment.is_blocked, Comment.parent_comment]
