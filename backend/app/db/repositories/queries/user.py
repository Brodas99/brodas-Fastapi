CREATE_USER_QUERY = """
    INSERT INTO users_v1 (firstname, lastname, username, email, salt, password)
    VALUES (:firstname, :lastname, :username, :email, :salt, :password)
    RETURNING id, firstname, lastname, username, email, email_verified, salt, password, is_active, created_at, updated_at;
"""

GET_USER_BY_ID_QUERY = """
    SELECT
        id, 
        firstname,
        lastname,
        username,
        email,
        created_at,
        updated_at
    FROM users_v1
    WHERE id = :id;
"""


GET_ALL_USERS_QUERY = """
    SELECT
        id, 
        firstname,
        lastname,
        username,
        email,
        email_verified,
        is_active,
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


UPDATE_USER_BY_ID_QUERY = """
    UPDATE users_v1
    SET firstname  = :firstname,  
        lastname   = :lastname,  
        username   = :username,  
        email      = :email  
        password   = :password
    WHERE id = :id  
    RETURNING id, firstname, lastname, username, email; 
"""