import json
import logging
import typing as t
from http import HTTPStatus

from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError

from recommends.request_options import GetRecommendationSkuOption
from recommends.search_recommendations import search_recommendations

LOGGER = logging.getLogger(__name__)


class RecommendsView(MethodView):
    __GET_RECOMMENDATION_SKU_SCHEMA = GetRecommendationSkuOption.schema()

    def get(self) -> [t.Dict[str, t.Any], HTTPStatus]:
        try:
            request_body: GetRecommendationSkuOption = self.__GET_RECOMMENDATION_SKU_SCHEMA.load(request.args.to_dict())
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValidationError) as exception:
            return self.__return_bad_request(exception)
        try:
            result = search_recommendations(request_body.sku, request_body.rec_min)

        except FileNotFoundError as exception:
            return jsonify(
                {
                    'error': str(exception)
                }
            ), HTTPStatus.NOT_FOUND

        return jsonify(
            {
                'result': result
            }
        )

    @staticmethod
    def __return_bad_request(exception: t.Any):
        LOGGER.warning('Request body is invalid.', exc_info=exception)
        return jsonify(
            {
                'error': 'request body is invalid.'
            }
        ), HTTPStatus.BAD_REQUEST
