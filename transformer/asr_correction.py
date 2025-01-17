import re
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry
import os

@registry.register_problem
class AsrCorrection(text_problems.Text2TextProblem):
  """Generate the correct transcription from the errored ASR output"""

  @property
  def approx_vocab_size(self):
    return 2**15  # ~32k

  @property
  def is_generate_per_split(self):
    # generate_data will shard the data into TRAIN and EVAL for us.
    return True

  @property
  def dataset_splits(self):
    """Splits of data to produce and number of output shards for each."""
    # 10% evaluation data
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 9,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    del data_dir
    del tmp_dir
    #del dataset_split
    
    train = dataset_split == problem.DatasetSplit.TRAIN

    if train:
      print("TRAIN")
      root_dir="/speech/epoch13_5gram_transcriptions/train/"
    else:
      print("VAL")
      root_dir="/speech/epoch13_5gram_transcriptions/dev/"
    csv_files = os.listdir(root_dir)
    for csv_file in csv_files:
      filename = root_dir + csv_file
      with open(filename, 'r') as f:
          content = f.readlines()
          for row in content:
              prediction = row.split(',')[1]
              truth = row.split(',')[2]
              if prediction == "" or prediction == " ":
                continue
              yield {"inputs": prediction, "targets": truth }
    #for i in range(0,100):
    #  prediction = ""
    #  truth = ""
    #  yield {"inputs": prediction, "targets": truth }
