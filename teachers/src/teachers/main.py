#!/usr/bin/env python
import sys
import warnings
import os


# Disable LiteLLM proxy & telemetry completely
os.environ["LITELLM_PROXY"] = "false"
os.environ["LITELLM_DISABLE_TELEMETRY"] = "true"
os.environ["LITELLM_DISABLE_SPEND_LOGGING"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from .crew import Teachers

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': "explain me linked list in C ",
        'current_year': str(datetime.now().year)
    }
    r=Teachers().crewcall()
    result=r.kickoff(inputs=inputs)
    print(result.raw)
if __name__=="__main__":
    run()

