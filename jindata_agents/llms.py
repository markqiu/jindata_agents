import os

from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

oai_api_key = os.getenv("OPENAI_API_KEY", "null")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

openai_gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.4, api_key=oai_api_key)
openai_gpt4 = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.5)


def ollama_factory(base_url=ollama_base_url, model="notux", temperature=0):
    return Ollama(base_url=base_url, model=model, temperature=temperature)


ollama_notux = ollama_factory(base_url=ollama_base_url, model="notux", temperature=0)
ollama_yi = ollama_factory(base_url=ollama_base_url, model="yi", temperature=0)
mixtral = ollama_factory(model="mixtral")
hub_based_dolphin_mixtral = ollama_factory(model="hub/based-dolphin-mixtral")
codellama = ollama_factory(model="codellama:70b")
codeup = ollama_factory(model="codeup:latest")
deepseek_coder = ollama_factory(model="deepseek-coder:33b")
dolphin_mixtral = ollama_factory(model="dolphin-mixtral:latest")
gemma = ollama_factory(model="gemma:latest")
mixtral = ollama_factory(model="mixtral")
nexusraven = ollama_factory(model="nexusraven:latest")
notux = ollama_factory(model="notux")
nous_hermes2 = ollama_factory(model="nous-hermes2:latest")
openhermes = ollama_factory(model="openhermes:latest")
phind_codellama = ollama_factory(model="phind-codellama:latest")
qwen_14b = ollama_factory(model="qwen:14b")
qwen_72b = ollama_factory(model="qwen:72b")
yarn_mistral = ollama_factory(model="yarn-mistral:latest")
yi = ollama_factory(model="yi")
zephyr = ollama_factory(model="zephyr")
openchat = ollama_factory(model="openchat:latest")
