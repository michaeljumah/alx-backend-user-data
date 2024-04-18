#!/usr/bin/env python3
"""Session authentication module for the API.
"""


from uuid import uuid4

from models.user import User

from .auth import Auth


class SessionAuth(Auth):
    """Session authentication class that inherits from Auth class.

    Args:
        Auth (type): Class inherited from.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id.

        Args:
            user_id (str, optional): The ID of user to create a session for.
            Defaults to None.

        Returns:
            str: The session ID if the user ID is valid, None otherwise.
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID for a given session ID.

        Args:
            session_id (str, optional): The session ID to retrieve the user
            ID for.
            Defaults to None.

        Return None if session_id is None.
        Return None if session_id is not a string.
        Return the value (the User ID) for the key session_id in the dictionary
        user_id_by_session_id.

        Returns:
            str: The user ID if the session ID is valid, None otherwise.
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Returns a User instance based on a cookie value.

        Args:
            request (flask.request, optional): The request object containing
            the session cookie.. Defaults to None.

        Use self.session_cookie(...) & self.user_id_for_session_id(...)
        to return the User ID based on the cookie _my_session_id.

        Returns:
            User: A User instance, if a User can be found based on the value
            of the cookie. Otherwise, returns None.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Delete the user session (log out the user) based on the session
        ID cookie in the request.

        Args:
            request (flask.request, optional): The Flask request object.
            Defaults to None.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
    
