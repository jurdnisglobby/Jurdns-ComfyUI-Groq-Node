from pathlib import Path
import sys

# Get the directory of the current file and add it to the Python path
NODE_DIRECTORY = Path(__file__).parent
sys.path.insert(0, str(NODE_DIRECTORY))

print("Loading Jurdns Groq Node...")

try:
    from .jurdns_groq_node import JurdnsGroqAPIPromptEnhancer
    print("Successfully imported JurdnsGroqAPIPromptEnhancer")
except ImportError as e:
    print(f"ImportError: {e}")
    # Optionally, you can handle the error here, such as by logging or exiting
except Exception as e:
    print(f"Other Error: {e}")
    # Handle other exceptions

NODE_CLASS_MAPPINGS = {
    "JurdnsGroqAPIPromptEnhancer": JurdnsGroqAPIPromptEnhancer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JurdnsGroqAPIPromptEnhancer": "Jurdn's Groq API Prompt Enhancer"
}

print("Jurdns Groq Node init complete.")