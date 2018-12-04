import ores.api
import yaml

# TODO: wire the feature switch
include_features = False
model_names = [
    'damaging',
    'itemquality',
]
ores_host = 'https://ores.wikimedia.org'
parallel_requests = 4
user_agent = 'Example app, contact awight@wikimedia.org'
wiki_context = 'wikidatawiki'


def score_wikidata_revisions(rev_ids):
    session = ores.api.Session(ores_host, user_agent=user_agent, parallel_requests=parallel_requests)
    scores = session.score(wiki_context, model_names, rev_ids)
    return scores


if __name__ == '__main__':
    sample_revisions = [123456, 654321]
    scores = score_wikidata_revisions(sample_revisions)
    # FIXME: The "zip" should have been unnecessary.
    print(yaml.safe_dump(dict(zip(sample_revisions, scores))))
