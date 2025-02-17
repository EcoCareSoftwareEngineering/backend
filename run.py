if __name__ == "__main__":

    from app import create_app

    app, socketio = create_app()
    socketio.run(app=app, host="0.0.0.0", debug=True, allow_unsafe_werkzeug=True)
