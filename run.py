from app import create_app

my_flask_app = create_app()

if __name__ == "__main__":
    my_flask_app.run(debug=True)
