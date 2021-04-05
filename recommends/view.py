import logging

from flask.views import MethodView

LOGGER = logging.getLogger(__name__)


class RecommendsView(MethodView):
    def get(self):
        pass
