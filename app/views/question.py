from flask import Blueprint
from flask.views import MethodView

question_blueprint = Blueprint('question', __name__)


class QuestionGetAPI(MethodView):
    def get(self):
        return '<h1>Hello Question!</h1>'


quest_get_view = QuestionGetAPI.as_view('quest_get_api')

question_blueprint.add_url_rule(
    '/question/get',
    view_func=quest_get_view,
    methods=['GET']
)
