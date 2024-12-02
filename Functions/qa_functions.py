import aiohttp

# This class contains functions that are used to interact with the LLM Chatbot model using the API endpoint.
# It also contains the context that is used to generate the completions. This context will be retrieved during the initialization of the class.
class Qa_Functions:
    def __init__(self, pc_path: str, pn_path: str):
        # Set the API URL
        self.api_url = "http://localhost:1234/v1/chat/completions"

        # Get the context from the text files
        with open(pc_path, "r") as file:
            self.pc_context = file.read()
        
        with open(pn_path, "r") as file:
            self.pn_context = file.read()
        
        # Set the messages for Primal Chaos. This will be used to help the model to distinguish between related questions and unrelated questions.
        self.pc_messages = [
            { "role": "assistant", "content": "Hello. I am the Primal Chaos Helper ready to answer any question you have about Primal Chaos" },
            { "role": "user", "content": "What is the capital in france?" },
            { "role": "assistant", "content": "Not enough information to fulfill request." },
            { "role": "user", "content": "Who is the final boss in Primal" },
            { "role": "assistant", "content": "The final boss in Primal Chaos is currently the Deathknight. He can be summoned and if he's defeated there is a 10% chance he drops a tameable token." },
            { "role": "user", "content": "Write me a poem" },
            { "role": "assistant", "content": "Not enough information to fulfill request." },
            { "role": "user", "content": "Tell me a bit about the Elemental tier" },
            { "role": "assistant", "content": "The Volcanic elemental is weak against the Hydro Elementals but it is stronger against the Electric." },
            { "role": "user", "content": "What did I just say?" },
            { "role": "assistant", "content": "Not enough information to fulfill request." },
            { "role": "user", "content": "What are spawncodes?" },
            { "role": "assistant", "content": "The spawncodes can be found on the spreadsheet: https://docs.google.com/spreadsheets/d/1cT7InAARC7WxlWVByin3DLlLE5HZ1e6P93UNyO2Kl1A/edit?usp=sharing" },
            ]
        self.pn_messages = []


    # This function sends a request to the API endpoint to generate completions for the given prompt.
    async def generate_completions(self, prompt, is_primal_chaos):
        # The headers to indicate that we are sending JSON data
        headers = {
            "Content-Type": "application/json"
        }

        # Get the lines depending on the "is_primal_chaos" parameter
        lines = self.pc_context if is_primal_chaos else self.pn_context

        # The JSON data payload
        data = {
            "messages": [
            { "role": "system", "content": "You are a chatbot designed to provide information and answer questions specifically related to Primal Chaos. You should only respond to queries that directly relates to the given context. If a query is unrelated to the context, respond with: 'Not enough information to fulfill request.'" },
            { "role": "user", "content": lines }
            ],
            "temperature": 0.3,
            "max_tokens": -1,
            "stream": False
        }

        if is_primal_chaos:
            data["messages"].extend(self.pc_messages)
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