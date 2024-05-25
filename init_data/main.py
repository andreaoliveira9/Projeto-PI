from user import init_users, login_users
from offer import init_offers, init_images, init_reviews, init_payments


def main():
    init_users()
    token_array = login_users()
    init_offers(token_array)
    init_images(token_array)
    init_reviews(token_array)
    init_payments(token_array)


if __name__ == "__main__":
    main()
