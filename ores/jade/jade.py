import json
import logging
import mwapi

log = logging.getLogger(__name__)

JADE_PSEUDO_MODEL = "judgment"
JADE_VERSION = "0.0.0"


def process_create_judgment(config, scoring_system, context, rev_id):
    log.info("Creating judgment for {} at revision {}".format(context, rev_id))

    judgment = fetch_judgment(config, context, rev_id)

    store_judgment(scoring_system, context, rev_id, judgment)


def store_judgment(scoring_system, context, rev_id, judgment):
    entity_rev_id = judgment["entity"]["rev_id"]

    # TODO: Make this part of the scoring_system API.
    scoring_system.score_cache.store(
        judgment, context, JADE_PSEUDO_MODEL, entity_rev_id,
        version=JADE_VERSION, injection_cache={})


def process_suppress_judgment(config, scoring_system, context, rev_id, event):
    log.info("Suppressing judgment for {} at revision {}, with data {}".format(
        context, rev_id, json.dumps(event)))


def fetch_judgment(config, context, rev_id):
    api_config = config["jade"]["mwapi"][context]
    session = mwapi.Session(**api_config)
    params = {
        "action": "query",
        "prop": "revisions",
        "revids": rev_id,
        "rvprop": ["timestamp", "user", "userid", "comment", "content"],
    }
    doc = session.get(**params)
    page_docs = doc["query"].get("pages", {}).values()
    if len(page_docs) != 1:
        log.warn("Bad JADE revision received: {}".format(rev_id))
        return

    rev_doc = list(page_docs)[0]["revisions"][0]
    judgment = _normalize_judgment(rev_doc)
    return judgment


def _normalize_judgment(rev_doc):
    meta_fields = ["timestamp", "user", "userid", "comment"]

    judgment = json.loads(rev_doc["*"])
    judgment["meta"] = {key: rev_doc[key] for key in rev_doc.keys()
        where key in meta_fields}

    return judgment
