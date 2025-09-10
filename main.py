import os
import hydra
from omegaconf import DictConfig
from utils.utils import init_client

@hydra.main(version_base=None, config_path='cfg', config_name='config')
def main(cfg: DictConfig):
    print(f'Memory size: {cfg.algorithm.memory_size}')
    print(f"Using LLM: {cfg.get('model', cfg.llm_client.model)}")
    
    client = init_client(cfg)

if __name__ == '__main__':
    main()