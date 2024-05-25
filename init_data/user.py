import json
import psycopg2
import os


def init_users():
    # read json file
    file = open("data/users.json", "r")
    users = json.load(file)
    file.close()

    # connect to postgress database
    conn = psycopg2.connect(
        host="localhost",
        database="user_db",
        user="user_db_user",
        password="user_db_password",
    )
    cur = conn.cursor()

    # insert users into database

    for user in users:
        cur.execute(
            'INSERT INTO usr_microservice."user" (id, email, f_name, l_name, phone_number, roles, verified, tags, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (
                user["uid"],
                user["email"],
                user["f_name"],
                user["l_name"],
                user["phone_number"],
                user["roles"],
                user["verified"],
                user["tags"],
                user["image"],
            ),
        )
    conn.commit()
    cur.close()
    conn.close()


def login_users():
    file = open("data/users.json", "r")
    users = json.load(file)
    file.close()

    # get api key from .env file
    file = open(".env", "r")
    env = file.read()
    file.close()
    api_key = env.split("=")[1]

    firebase_token_array = {}
    token_array = {}
    for user in users:
        curl_string = f"""curl 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}' \
           -H 'Content-Type: application/json' \
           --data-binary '{{"email":"{user['email']}","password":"demo_password","returnSecureToken":true}}'"""

        # change email and password
        # execute curl command
        response = os.popen(curl_string).read()
        response = json.loads(response)
        firebase_token_array[user["uid"]] = response["idToken"]

    for uid, token in firebase_token_array.items():
        api_string = f"""curl -X 'POST' 'http://localhost:8000/api/user/login' \
                -H 'accept: application/json' \
                -H 'Authorization: Bearer {token}' \
                -d ''"""

        # execute api call
        response = os.popen(api_string).read()
        response = json.loads(response)
        token_array[uid] = response["access_token"]

    return token_array
