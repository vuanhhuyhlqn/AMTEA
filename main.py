import os
import hydra
from omegaconf import DictConfig

from LLM.model import GPTModel

@hydra.main(version_base=None, config_path='cfg', config_name='config')
def main(cfg: DictConfig):
    print(f'Algorithm: {cfg.algorithm}')
    print(f'LLM Model: {cfg.llm_client.model}')
    


if __name__ == '__main__':
    main()