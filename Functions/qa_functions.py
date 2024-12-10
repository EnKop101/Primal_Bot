import aiohttp
from Classes.qa_class import QA_Class

# This class contains functions that are used to interact with the LLM Chatbot model using the API endpoint.
# It also contains the context that is used to generate the completions. This context will be retrieved during the initialization of the class.
class Qa_Functions:
    def __init__(self, pc_messages: list[QA_Class], pn_messages: list[QA_Class]):
        # Set the API URL
        self.api_url = "http://localhost:1234/v1/chat/completions"

        
        # Set the messages for Primal Chaos. This will be used to help the model to distinguish between related questions and unrelated questions.
        self.pc_messages = self.format_messages(pc_messages)
        self.pn_messages = self.format_messages(pn_messages)

        self.pc_context = self.get_context(pc_messages)
        self.pn_context = self.get_context(pn_messages)


    # This function sends a request to the API endpoint to generate completions for the given prompt.
    async def generate_completions(self, prompt, is_pc):
        # The headers to indicate that we are sending JSON data
        headers = {
            "Content-Type": "application/json"
        }

        # Get the lines depending on the "is_primal_chaos" parameter
        messages = self.pc_messages if is_pc else self.pn_messages
        context = self.pc_context if is_pc else self.pn_context

        # The JSON data payload to send to the API endpoint
        data = {
            "messages": [
            { "role": "system", "content": """You are a helpful and informative AI assistant. Your task is to accurately answer questions based on the provided conversation history and context. If a question is unrelated to the previous conversation, Answer 'I do not have any information about this topic.'""" },
            { "role": "user", "content": "CONTEXT:\n " + context },
            { "role": "assistant", "content": "Okay I'm ready." },
            ],
            "temperature": 0.3,
            "max_tokens": -1,
            "stream": False
        }
        
        if is_pc:
            data["messages"].extend(messages)
        else:
            # To be implemented
            pass

        # Add the user prompt to the messages
        data["messages"].append({ "role": "user", "content": prompt })

        # Making the POST request to the local server
        return await self.fetch_response(headers, data)

    async def fetch_response(self, headers, data):
    
        # Make the request using aiohttp
        async with aiohttp.ClientSession() as session:
            try:
                # Make the POST request
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    # Check if the response is successful
                    if response.status == 200:
                        jsonData = await response.json()
                        first_choice = jsonData["choices"][0]
                        content = first_choice["message"]["content"]
                        return content
                    else:
                        # If the response is not successful, print the status and the response message
                        print("\n-------------------\nFailed to get response:", response.status, await response.text())
                        return None
            except Exception as e:
                # If an error occurred, print the error
                print("\n-------------------\nAn error occurred:", str(e))
                return None
    
    def format_messages(self, messages):
        formatted_messages = []
        for message in messages:
            formatted_messages.append({"role": "user", "content": message.question.replace("!!!", "")})
            formatted_messages.append({"role": "assistant", "content": message.answer})
        return formatted_messages
    
    def get_context(self, messages: list[QA_Class]):
        context = ""
        for message in messages:
            if "!!!" not in message.question:
                context += f"{message.answer}\n"
        
        return context
    
    async def update_qaf_variables(self, messages: list[QA_Class], is_pc: bool):
        if is_pc:
            self.pc_messages = self.format_messages(messages)
            self.pc_context = self.get_context(messages)
        else:
            self.pn_messages = self.format_messages(messages)
            self.pn_context = self.get_context(messages)