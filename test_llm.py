from getParas import Paras
from utils.utils import init_client

class TestLLM:
    def __init__(self, cfg, client) -> None:
        self.cfg = cfg
        
        self.paras = Paras()
        self.paras.set_paras(llm_model = client)
        
        init_client(cfg)
        
    def run(self):
        pass