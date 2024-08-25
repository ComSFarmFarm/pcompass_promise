from flask import Flask

from controller import main
from controller import promise


def create_app(): # 애플리케이션 팩토리 -> 쉽게 말해 app 객체를 생성하여 반환하는 함수
    app = Flask(__name__)

    app.register_blueprint(main.bp)
    app.register_blueprint(promise.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000)