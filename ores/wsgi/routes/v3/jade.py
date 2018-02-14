# TODO:
# * Wrap processing in a Celery task

import logging

from flask import request

from ores.jade import process_create_judgment, process_suppress_judgment
from ores.wsgi import preprocessors, responses, util

logger = logging.getLogger(__name__)


def configure(config, bp, scoring_system):

    @bp.route("/v3/jade/<context>/create/<int:rev_id>", methods=["POST"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def create_judgment_v3(context, rev_id):
        try:
            process_create_judgment(config, scoring_system, context, rev_id)
            return responses.no_content()
        except Exception as e:
            return responses.bad_request(str(e))

    @bp.route("/v3/jade/<context>/suppress/<int:rev_id>", methods=["POST"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def suppress_judgment_v3(context, rev_id):
        try:
            event = request.get_json()
            process_suppress_judgment(config, scoring_system, context, rev_id, event)
            return responses.no_content()
        except Exception as e:
            return responses.bad_request(str(e))

    return bp
