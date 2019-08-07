import re

#from gutenberg import acquire
#from gutenberg import cleanup
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry

@registry.register_problem
class AsrCorrection(text_problems.Text2TextProblem):
  """Predict next line of poetry from the last line. From Gutenberg texts."""

  @property
  def approx_vocab_size(self):
    return 2**13  # ~8k

  @property
  def is_generate_per_split(self):
    # generate_data will shard the data into TRAIN and EVAL for us.
    return False

  @property
  def dataset_splits(self):
    """Splits of data to produce and number of output shards for each."""
    # 10% evaluation data
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 8,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 2,
    }]

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    del data_dir
    del tmp_dir
    del dataset_split

    with open('/speech/german-single-speaker-transcriptions/german-single-speaker-transcriptions.csv', 'r') as f:
        content = f.readlines()
        for row in content:
            prediction = row.split(',')[0]
            truth = row.split(',')[1]
            yield {"inputs": prediction, "targets": truth }

    #books = [
        # bookid, skip N lines
    #    (19221, 223),
    #    (15553, 522),
    #]
    '''
    for (book_id, toskip) in books:
      text = cleanup.strip_headers(acquire.load_etext(book_id)).strip()
      lines = text.split("\n")[toskip:]
      prev_line = None
      ex_count = 0
      for line in lines:
        # Any line that is all upper case is a title or author name
        if not line or line.upper() == line:
          prev_line = None
          continue

        line = re.sub("[^a-z]+", " ", line.strip().lower())
        if prev_line and line:
            yield {"inputs": prev_line, "targets": line }
            ex_count += 1
        prev_line = line
    '''