from revscoring import Model
from revscoring.scoring import ModelInfo


class JadeScorer(Model):
    """
    Glue to make JADE judgments behave like other scoring.
    """
    def __init__(self, version=None):
        super().__init__([], version=version)
        self.info = ModelInfo()
        self.info['version'] = version
        self.info['type'] = "JadeScorer"
        self.info['behavior'] = "Returns JADE judgments as a score"

    def score(self, feature_values):
        # TODO: Fetch from the MW API only very rare circumstances, i.e. only
        # when the item may have fallen out of the LRU cache.

        # FIXME: How should "no score" be represented?
        return {}

    @classmethod
    def from_config(cls, config, name, section_key='scorer_models'):
        section = config[section_key][name]
        return cls(**{k: v for k, v in section.items() if k != "class"})
