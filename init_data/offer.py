import json
import os


def init_offers(token_array):
    # read json file
    file = open("data/offers.json", "r")
    offers = json.load(file)
    file.close()

    for offer in offers:
        # connect to postgress database
        uid = offer["userid"]
        curl_string = f"""curl -X 'POST' 'http://localhost:8002/api/offer/' \
            -H 'Content-Type: application/json' \
            -H 'accept: application/json' \
            -H 'Authorization: Bearer {token_array[uid]}' \
            -d '{json.dumps(offer)}'"""

        os.system(curl_string)


def init_images(token_array):
    # get all folders in images
    folders = os.listdir("images")
    offers = json.load(open("data/offers.json", "r"))
    for folder in folders:
        # get all files in folder
        files = os.listdir(f"images/{folder}")
        uid = offers[int(folder) - 1]["userid"]
        for file in files:
            print(f"Uploading {file} from {folder}")
            file_extension = file.split(".")[-1]
            # connect to postgress database
            print(file_extension)
            curl_string = f"""curl -X 'POST' 'http://localhost:8002/api/offer/image/{folder}' \
                -H 'Content-Type: multipart/form-data' \
                -H 'accept: application/json' \
                -H 'Authorization: Bearer {token_array[uid]}' \
                -F 'file=@images/{folder}/{file};type=image/{file_extension}'"""

            os.system(curl_string)


def init_reviews(token_array):
    # read json file
    file = open("data/reviews.json", "r")
    reviews = json.load(file)
    file.close()

    # key is the offer id
    for key in reviews:
        # in each review, theres a uid : review
        for uid in reviews[key]:
            # connect to postgress database
            user_token = token_array[uid]
            review = reviews[key][uid]
            data = {"comment": review, "score": 0, "userid": uid, "offerid": key}

            curl_string = f"""curl -X 'POST' 'http://localhost:8002/api/offer/review/' \
                -H 'Content-Type: application/json' \
                -H 'accept: application/json' \
                -H 'Authorization: Bearer {user_token}' \
                -d '{json.dumps(data)}'"""

            os.system(curl_string)


def init_payments(token_array):
    file = open("data/payments.json", "r")
    payments = json.load(file)
    file.close()

    for payment in payments:
        uid = payment["userid"]
        curl_string = f"""curl -X 'POST' 'http://localhost:8004/api/payment/' \
            -H 'Content-Type: application/json' \
            -H 'accept: application/json' \
            -H 'Authorization: Bearer {token_array[uid]}' \
            -d '{json.dumps(payment)}'"""

        os.system(curl_string)
