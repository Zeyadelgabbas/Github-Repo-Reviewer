import json
import tiktoken
from openai import OpenAI
from typing import Dict , Optional 

from ..utils import config , get_logger

logging = get_logger(__name__)


class LLMTools:

    """"
    tools for interacting with OPENAI models
    """

    def __init__(self):

        self.model_name = config.model_name
        self.temperature = float((config.temperature))
        self.max_tokens = config.max_tokens

        self.client = OpenAI(api_key=config.openai_api_key)



    def call_gpt(
            self,
            user_prompt: str,
            system_prompt: str,
            response_format: str = "text",
            temperature :  Optional[float] = None ,
            max_tokens  : Optional[int] = None) -> str:
    

        """ 
        calls LLM and get response
        
        returns : LLM response as string
        
        """

        temperature = self.temperature if not temperature else temperature
        max_tokens = self.max_tokens if not max_tokens else max_tokens
        if self.model_name == 'gpt-5':
            temperature = 1

        try:

            messages = [
                {'role':'system' , 'content':system_prompt},
                {'role':'user','content':user_prompt}
            ]

            messages = self._format_messages(messages=messages)
            response = self.client.responses.create(
                model = self.model_name,
                input=messages,
                temperature=temperature,
                max_output_tokens = max_tokens
            )

            response_text = response.output_text
            print(response_text)
            x=response.model_dump_json(indent=2)
            logging.info(f"output new : \n\n {x}")

            print(response.model_dump_json(indent=2))

            logging.info(f"response text : {response_text}")

            total_tokens = response.usage.total_tokens
            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens

            logging.info("LLM response recevied")
            logging.info(f"total tokens used : {total_tokens} , prompt tokens : {prompt_tokens} , completion tokens : {completion_tokens}")

            if response_format == 'json':
                self._validate_json(response_text)
                

            return response_text

        except json.JSONDecodeError as e:
            error_msg = f"LLM returned invalid json : {e}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        except Exception as e:
            error_msg=f"Error calling gpt : {e}"
            logging.error(error_msg)
            raise e
    



    def _validate_json(self,response_text :str) ->None:

        try:
            logging.info(f" the respone is \n\n {response_text}")
            json.loads(response_text)
            logging.info("response valid as json")

        except json.JSONDecodeError as e:
            logging.error(f"Invalid json response : {e}")
            raise e 
        

    def estimate_token_cost(self,text: str, input_price_per_million: float = None, output_price_per_million: float = None, expected_output_tokens: int = None) -> dict:
        """
        Estimate token usage and cost for any text, given prices per 1M tokens.

        Args:
            text (str): Input text or prompt.
            input_price_per_million (float): Input price in USD per 1 million tokens.
            output_price_per_million (float): Output price in USD per 1 million tokens.
            expected_output_tokens (int): Estimated number of tokens in the model's response.

        Returns:
            dict: Token count and cost estimate.
        """

        if not expected_output_tokens:
            expected_output_tokens = self.max_tokens

        if not input_price_per_million:
            input_price_per_million = config.get("agent.input_price")
        if not output_price_per_million:
            output_price_per_million = config.get("agent.output_price")

        encoding = tiktoken.get_encoding("cl100k_base")
        input_tokens = len(encoding.encode(text))
        logging.info(f"total tokens :  {(input_tokens)} tokens")
        input_cost_per_token = input_price_per_million / 1_000_000
        output_cost_per_token = output_price_per_million / 1_000_000

        # Compute costs
        input_cost = input_tokens * input_cost_per_token
        output_cost = expected_output_tokens * output_cost_per_token
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": input_tokens,
            "output_tokens_est": expected_output_tokens,
            "total_tokens_est": input_tokens + expected_output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6)
        }




    def _format_messages(self,messages):
        """Convert old-style messages into new API-compatible format."""

        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg["role"],
                "content": [{"type": "input_text", "text": msg["content"]}]
            })
        return formatted
        