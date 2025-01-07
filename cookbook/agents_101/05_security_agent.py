from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.spider import SpiderTools
import configparser
import os

class Config:
    def __init__(self, config_file='~/.config/ticonfig.ini'):
        self.config_file = os.path.expanduser(config_file)
        self.host = None
        self.model_id = None
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_file):
            print(f"Configuration file '{self.config_file}' does not exist.")
            return
        
        config = configparser.ConfigParser()
        try:
            config.read(self.config_file)
            self.host = config.get('agent', 'host', fallback=None)
            self.model_id = config.get('agent', 'model_id', fallback=None)
        except configparser.Error as e:
            print(f"Error reading configuration file: {e}")

class TemplateLoader:
    def __init__(self, template_file='~/.config/template.txt'):
        self.template_file = os.path.expanduser(template_file)

    def load_template(self):
        try:
            with open(self.template_file, 'r') as file:
                return file.read().strip()
        except IOError as e:
            print(f"Error reading template file: {e}")
            return ("You are a cyber security analyst and should only answer questions regarding cyber security based on latest info. " + 
                    "Your answer should be insightful, by conducting research and analysis from multiple sources.")

config = Config()
if config.host and config.model_id:
    sec_agent = Agent(
        name="Security Agent",
        model=Ollama(id=config.model_id, host=config.host),
        tools=[DuckDuckGo()],
        show_tool_calls=True,
        read_chat_history=True,
        markdown=True
    )
    
    template_loader = TemplateLoader()
    
    while True:
        user_input = input("Enter your question (or 'quit' to exit): ")
        if user_input.lower() == "quit":
            break

        # Load the template each time before responding
        user_input_prefix = template_loader.load_template()
        sec_agent.print_response(f"{user_input_prefix} {user_input}", stream=True)
else:
    print("Model name or host not found in the configuration file.")