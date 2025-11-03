import json 
import os 
from typing import Dict , List , Any , Optional

from ..tools import FileScanner , LLMTools
from ..utils import get_logger 
from .state import AgentState
from ..prompts import get_comprehensive_review_prompt , get_system_prompt

logging = get_logger(__name__)

class CodeReviewer:

    """" 
    Code reviewer agent that reads the entire repository 

    1- read all code files
    2- concatenate all files with structure
    3- invoke LLM with entire structured repo cotent
    4- updates states with ( understanding , review , suggestions )
    """


    def __init__(self):
        
        self.llm = LLMTools()
        self.filescanner = FileScanner()


    def review(self,state: AgentState) -> AgentState:

        """
        Main review function that analyze the repo 
        """

        try:
            repo_name = state['repo_name']
            file_structure = state['file_structure']
            language_stats = self.filescanner._get_language_stats(files = state['files_to_review'])
            repo_content = self._concatenate_files(state=state)
            logging.info("repo content created for for user prompt")

            system_prompt = get_system_prompt()
            user_prompt = get_comprehensive_review_prompt(
                repo_name=repo_name,
                repo_content=repo_content,
                file_structure=file_structure,
                language_stats=language_stats
            )
            logging.info("user prompt formatted")

            response_json = self.llm.call_gpt(
                user_prompt=user_prompt,
                system_prompt=system_prompt,
                response_format='json'
            )
            logging.info("json response generated from LLM")

            structured_response = self._parse_json_response(response_json)
            logging.info("parsed analysis results succesfully")

            state_update = self._update_state(state= state , structured_response = structured_response)
            logging.info("code review agent updated states")

            return state_update
        
        except json.JSONDecodeError as e: 
            error_msg = f"failed to parse llm response as json : {str(e)}"
            logging.error(error_msg)
            raise error_msg
        
        except Exception as e:
            error_msg = f"Error reviewing {repo_name} : {e}"
            logging.error(error_msg)
            raise e 

    def _concatenate_files(self,state: AgentState) -> str:

        """ reads and concatenates all files into one string """

        try:

            all_files = state['files_to_review']
            repo_path = state['local_path']

            content = " "

            for file_path in all_files:
                content += f"\nFile : {file_path} \n\ncontent :\n\n{self.filescanner.read_file_content(repo_path,file_path)}\n\n"
                content += "==="*10

            logging.info(f"Concatenated {len(all_files)} files successfully")
            return content

        except Exception as e:
            error_msg = f"Error concatenating files : {e}"
            logging.error(error_msg)
            raise error_msg

    def _parse_json_response(self, response: str) -> Dict[str,Any]:

        """ Parses LLM json response into structured data"""

        try: 

            logging.info("Parsing GPT response...")
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]  # Remove ```json
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]  # Remove ```
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]  # Remove ```
        
            response_clean = response_clean.strip()

            analysis = json.loads(response_clean)
            logging.info("JSON parsed successfully")

            return analysis

        except json.JSONDecodeError as e:
            error_msg = f"error parsing json response : {str(e)}"
            logging.error(error_msg)
            raise error_msg
        
        except Exception as e: 
            logging.error(e)
            raise e


    def _update_state(self,state: AgentState , structured_response : Dict[str,Any]) -> AgentState:

        analysis = structured_response
        state["understanding"] = analysis.get("understanding", {})

        # Add code review findings
        state["code_review"] = analysis.get("code_review", {})
        
        # Add enhancement suggestions
        state["enhancements"] = analysis.get("enhancements", [])
        
        # Add documentation assessment
        state["documentation"] = analysis.get("documentation", {})
        
        # Add summary
        state["summary"] = analysis.get("summary", {})
        
        # Count issues
        code_review = state["code_review"]
        total_issues = (
            len(code_review.get("security", [])) +
            len(code_review.get("bugs", [])) +
            len(code_review.get("performance", [])) +
            len(code_review.get("code_quality", []))
        )
        
        state["total_issues_found"] = total_issues
        
        # Add success message
        message = f"✅ Analysis complete: Found {total_issues} issues across {len(state['files_to_review'])} files"
        state["messages"].append(message)
        
        logging.info(f"State updated: {total_issues} total issues found")
        
        return state
        
    def estimate_cost(self,state : AgentState):
            repo_name = state['repo_name']
            file_structure = state['file_structure']
            language_stats = self.filescanner._get_language_stats(files = state['files_to_review'])
            repo_content = self._concatenate_files(state=state)
            logging.info("repo content created for for user prompt")

            system_prompt = get_system_prompt()
            user_prompt = get_comprehensive_review_prompt(
                repo_name=repo_name,
                repo_content=repo_content,
                file_structure=file_structure,
                language_stats=language_stats
            )
            total_cost = self.llm.estimate_token_cost(text=user_prompt)['total_cost_usd']

            return total_cost
        
