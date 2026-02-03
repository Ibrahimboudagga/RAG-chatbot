import sys
import os

# Add src to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stores.LLM.template.template_parser import TemplateParser

tp = TemplateParser(language="en", default_language="en")
try:
    print("Trying to get rag system_prompt...")
    val = tp.get("rag", "system_prompt")
    print(f"Result: {val}")
except Exception as e:
    import traceback
    traceback.print_exc()
