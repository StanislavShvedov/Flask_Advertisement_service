import flask
from flask import jsonify, request
from flask.views import MethodView
from models import User, Advertisement, Session
from sqlalchemy.exc import IntegrityError
from errors import HttpError
from schema import validate, UpdateUserRequest, CreateUserRequest
from werkzeug.datastructures import ImmutableMultiDict

app = flask.Flask('add_service_app')


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    response = jsonify({'error': err.message})
    response.status_code = err.status_code
    return response


def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, message='пользователь с таким email уже зарегистрирован')


class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_json = validate(request.json, CreateUserRequest)
        user = User(name=user_json['name'], password=user_json['password'], email=user_json['email'])
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        user_json = validate(request.json, UpdateUserRequest)
        user = get_user_by_id(user_id)
        for filed, value in user_json.items():
            setattr(user, filed, value)
        request.session.commit()
        return jsonify(user.dict)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return 'Пользователь удален'


user_view = UserView.as_view('user')


def add_advertisement(advertisement: Advertisement):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(404, message='Только авторизованный ползователь может разместить объявление')


def get_advertisement_by_id(advertisement_id: int):
    advertisement = request.session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError(404, 'advertisement not found')
    return advertisement


class AdvertisementView(MethodView):

    def get(self, advertisement_id: int):

        advertisement = get_advertisement_by_id(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        advertisement_json = request.json
        advertisement = Advertisement(header=advertisement_json['header'],
                                      description=advertisement_json['description'],
                                      id_user=advertisement_json['id_user'])
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def patch(self, advertisement_id: int):

        owner_id = request.args.get('owner')
        advertisement_json = request.json
        advertisement = get_advertisement_by_id(advertisement_id)
        if advertisement.id_user != owner_id:
            raise HttpError(404, 'Менять объявление может только его владелец!')
        for filed, value in advertisement_json.items():
            setattr(advertisement, filed, value)
        request.session.commit()
        return jsonify(advertisement.dict)

    def delete(self, advertisement_id: int):

        owner_id = int(request.args.get('owner'))
        advertisement = get_advertisement_by_id(advertisement_id)
        if advertisement.id_user != owner_id:
            raise HttpError(409, 'Удалять обяъвление может только его владелец!')
        request.session.delete(advertisement)
        request.session.commit()
        return 'Объявление удалено'


advertisement_view = AdvertisementView.as_view('advertisement')

app.add_url_rule(
    '/api/v1/user',
    view_func=user_view,
    methods=['POST']
)

app.add_url_rule(
    '/api/v1/user/<int:user_id>',
    view_func=user_view,
    methods=['GET', 'PATCH', 'DELETE']
)

app.add_url_rule(
    '/api/v1/advertisement',
    view_func=advertisement_view,
    methods=['POST']
)

app.add_url_rule(
    '/api/v1/advertisement/<int:advertisement_id>',
    view_func=advertisement_view,
    methods=['GET', 'PATCH', 'DELETE']
)


if __name__ == '__main__':
    app.run()
