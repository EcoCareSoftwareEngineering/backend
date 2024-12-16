if __name__ == "__main__":

    from app import create_app

    create_app().run(host="0.0.0.0", debug=True)
