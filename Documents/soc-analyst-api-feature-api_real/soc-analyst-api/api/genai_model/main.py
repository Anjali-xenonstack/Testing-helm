from flask import Flask, jsonify, request
from pandasai.connectors import PostgreSQLConnector
from pandasai import Agent
from langchain_openai import AzureChatOpenAI
import os
import base64
import sys
import logging
import pandas as pd
from PIL import Image
import io
from langchain_community.agent_toolkits import create_sql_agent
from langchain.sql_database import SQLDatabase 
from langchain_openai import AzureChatOpenAI
from pandasai.connectors import PostgreSQLConnector
from pandasai import Agent
import os
import base64
from langchain.schema.runnable import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils.dbConfig import postgres_config

##### INIT #####
llm = AzureChatOpenAI(
    deployment_name="morepen4",
    openai_api_version="2024-02-15-preview",
    model_name="gpt-35-turbo",
    temperature=0.2,
    azure_endpoint="https://gpt4-openai-svc.openai.azure.com/",
    openai_api_key="a271732e5e25416095f030a7e01be485"
)


db_uri = "postgresql://"+postgres_config["username"]+":"+postgres_config["password"]+"@"+postgres_config["host"]+":"+str(postgres_config["port"])+"/"+postgres_config["database"]

# Database Connection 

db = SQLDatabase.from_uri(db_uri)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
postgres_connector = PostgreSQLConnector(config=postgres_config)
agent = Agent(postgres_connector, config={"llm": llm, "data_viz_library": "plotly", "enable_cache": False, "save_charts": True, "save_charts_path": "./base_64"})
##### INIT #####


def main_func():
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('query')
        logging.info("Received query: %s", query)
        
        if not query or query == "":
            logging.warning("No query provided or query is empty")
            return jsonify({
                'message': 'Bad Request',
                'error': True,
            }), 400
        
        try:
            logging.info("Initializing PostgreSQL connector")
            db_uri = "postgresql://"+postgres_config["username"]+":"+postgres_config["password"]+"@"+postgres_config["host"]+":"+str(postgres_config["port"])+"/"+postgres_config["database"]
            print("db_uri: ",db_uri)

            output_parser = StrOutputParser()
            router_prompt = PromptTemplate.from_template("""For queries about policies respond with `SQL_AGENT`. If the question is about plotting, respond with `pandas_agent`.

            Question: {question}""")
            router_chain = router_prompt | llm | output_parser


            logging.info("Creating Agent with PostgreSQL connector and LLM configuration")
            logging.info("Sending query to agent")
            print("Sending query to agent")
            chain = RunnableMap({
                    "action": router_chain,
                    "input": lambda x: x["question"]
                }) | select_chain 

            print("query: ",query)

            response = chain.invoke({'question': query})
        
            base_64_folder = './base_64'
            list_of_files = [os.path.join(base_64_folder, f) for f in os.listdir(base_64_folder) if f.endswith('.png')]
            
            if list_of_files:
                latest_file = max(list_of_files, key=os.path.getctime)
                
                with open(latest_file, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                
                os.remove(latest_file)
            else:
                base64_image = ""
            response_string = {}
            response_string['response']= response
            response_string['base_64_image']= base64_image
            if base64_image != "":
                response_string["width"], response_string["height"] = get_image_dimensions(base64_image)

            return jsonify({"data": response_string, "error":False}), 200
        
        except Exception as e:
            logging.error("Error occurred", exc_info=True)
            return jsonify({
                'message': 'Internal Server Error',
                'error': True,
            }), 500
    else:
        logging.warning("Method not allowed: %s", request.method)
        return jsonify({
            'message': '405 Method Not Allowed',
            'error': True,
        }), 405

def get_image_dimensions(base64_image):
    # Decode the base64 image string to bytes
    image_data = base64.b64decode(base64_image)

    # Open the image using PIL
    with io.BytesIO(image_data) as img_file:
        img = Image.open(img_file)
        width, height = img.size
        return width, height
    
def select_chain(output):
    if output["action"] == "SQL_AGENT":
        output[""]
        response = agent_executor.invoke({'input': output})
        return response['output'] if isinstance(response, dict) and 'output' in response else str(response)

    elif output["action"] == "pandas_agent":
        return agent.chat({'question': output['input']})
    else:
        return "Please repeat your question."
