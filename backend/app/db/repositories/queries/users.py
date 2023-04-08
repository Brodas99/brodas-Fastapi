CREATE_USER_QUERY = """
    INSERT INTO users_v1 (firstname, lastname, username, email, password, salt_password)
    VALUES (:firstname, :lastname, :username, :email, :password, :salt_password)
    RETURNING firstname, lastname, username, email
"""

GET_ALL_USERS_QUERY = """
    SELECT
        id, 
        firstname,
        lastname,
        username,
        email,
        created_at,
        updated_at
    FROM users_v1
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT
        id, 
        firstname,
        lastname,
        username,
        email,
        created_at,
        updated_at
    FROM users_v1
    WHERE email = :email;
"""

GET_USER_BY_USERNAME_QUERY = """
    SELECT 
        id,
        firstname,
        lastname,
        username
        email,
        created_at,
        updated_at
    FROM users_v1
    WHERE username = :username;
"""