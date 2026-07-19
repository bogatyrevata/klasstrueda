from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run(host="0", port=5000)

# поменять так чтобы применить класс TestingConfig для тестов, а не BaseConfig для разработки
