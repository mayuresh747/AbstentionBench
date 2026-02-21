import hydra
from hydra.core.global_hydra import GlobalHydra
from omegaconf import OmegaConf
from recipe.abstention_datasets.umwp import UMWP
from recipe.models import GPT51Rationalist
from recipe.inference import InferencePipeline
from torch.utils.data import SubsetRandomSampler

dataset = UMWP(data_dir="None/datasets/umwp")
print("len dataset:", len(dataset))

model = GPT51Rationalist()
pipeline = InferencePipeline(model, [dataset], save_dir="test_save")
pipeline.run(indices_subset=[0, 1, 2, 3, 4])
print("success!")
