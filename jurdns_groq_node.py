import json
import os
import subprocess
import sys
import stat

try:
    from groq import Groq, APITimeoutError, APIConnectionError
except ImportError:
    print("Installing groq library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
    from groq import Groq, APITimeoutError, APIConnectionError

class JurdnsGroqAPIPromptEnhancer:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "groq_config.json")
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"api_key": "", "system_prompt": ""}
            self.save_config()
            print(f"groq_config.json created. Please populate with your API key and system prompt at: {self.config_path}")
        except json.JSONDecodeError:
            print(f"Error decoding groq_config.json. Please ensure it is valid JSON at: {self.config_path}")
            self.config = {"api_key": "", "system_prompt": ""}
            self.save_config()
            print(f"groq_config.json created. Please populate with your API key and system prompt at: {self.config_path}")

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        os.chmod(self.config_path, stat.S_IRUSR | stat.S_IWUSR)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "override_system_prompt": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_text",)
    FUNCTION = "execute"
    CATEGORY = "Groq-Node"

    def execute(self, text, override_system_prompt=None):
        if not self.config["api_key"]:
            return ("Error: API key not configured. Please edit groq_config.json",)

        system_prompt_to_use = override_system_prompt if override_system_prompt is not None else self.config.get("system_prompt", "")

        client = Groq(api_key=self.config["api_key"])

        messages = []
        if system_prompt_to_use:
            messages.append({"role": "system", "content": system_prompt_to_use})
        messages.append({"role": "user", "content": text})

        try:
            # Use non-streaming request to get the full response at once
            completion = client.chat.completions.create(
                model="gemma2-9b-it",  # Use the model you need
                messages=messages,
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False  # Set stream to False for a regular response
            )
            return (completion.choices[0].message.content,)

        except APITimeoutError as e:
            return (f"Groq API Timeout Error: {e}",)
        except APIConnectionError as e:
            return (f"Groq API Connection Error: {e}",)
        except Exception as e:
            return (f"Groq API Error: {e}",)

NODE_CLASS_MAPPINGS = {
    "JurdnsGroqAPIPromptEnhancer": JurdnsGroqAPIPromptEnhancer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JurdnsGroqAPIPromptEnhancer": "Jurdn's Groq API Prompt Enhancer"
}