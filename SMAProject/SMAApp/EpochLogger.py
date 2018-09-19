from gensim.test.utils import common_texts as sentences
from gensim.models.callbacks import CallbackAny2Vec, PerplexityMetric, Callback
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
class EpochSaver():
    "Callback to save model after every epoch"
    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 0
    def on_epoch_end(self, model):
        output_path = '{}_epoch{}.model'.format(self.path_prefix, self.epoch)
        print("Save model to {}".format(output_path))
        model.save(output_path)
        self.epoch += 1
        
class EpochLogger(PerplexityMetric):
    "Callback to log information about training"
    def __init__(self):
        self.epoch = 0
        self.logger = None
        self.title = None

    def get_value(self, **kwargs):
        print("Epoch #{} ends".format(self.epoch))

        self.epoch += 1