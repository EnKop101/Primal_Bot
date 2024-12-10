import json
import os
from Classes.qa_class import QA_Class

# This class is the Data handling class for the Bot. It contains all the functions to interact with the json data files.
class DH_Functions:
    def __init__(self, pc_path: str, pn_path: str):
        # Set the paths for the json files.
        self.pc_path = pc_path
        self.pn_path = pn_path

        # Initialize the messages lists.
        self.pc_messages: list[QA_Class] = []
        self.pn_messages: list[QA_Class] = []

        # Check if the file exists. If it does not. Create folders and files.
        self.pc_messages = self.check_file_exists(pc_path)
        self.pn_messages = self.check_file_exists(pn_path)

    # This function adds a message to the json messages list.
    async def add_message(self, message: QA_Class, is_pc: bool):
        # Check is_pc to determine which list to add the message to.
        if is_pc:
            self.pc_messages.append(message)
            # Call the update function to update the json file.
            await self.update_json(self.pc_messages, self.pc_path)
            return self.pc_messages

        elif not is_pc:
            self.pn_messages.append(message)
            # Call the update function to update the json file.
            await self.update_json(self.pn_messages, self.pn_path)
            return self.pn_messages
    
    # This function removes a message from the json messages list by uuid.
    async def remove_message(self, message_id: str, is_pc: bool):
        # Check is_pc to determine which list to remove the message from.
        # Loop through the messages and remove the message with the matching id.
        if is_pc:
            for message in self.pc_messages:
                if message.id == message_id:
                    self.pc_messages.remove(message)
                    # Call the update function to update the json file.
                    await self.update_json(self.pc_messages, self.pc_path)
                    return self.pc_messages
            return None
        else:
            for message in self.pn_messages:
                if message.id == message_id:
                    self.pn_messages.remove(message)
                    # Call the update function to update the json file.
                    await self.update_json(self.pn_messages, self.pn_path)
                    return self.pn_messages
            return None

#region Private Functions.
    
    # This function updates the json file with the new messages.
    async def update_json(self, messages: list[QA_Class], file_path: str):
        # Update the message from the json file / Rewrite the file with the new messages.
        with open(file_path, "w") as file:
            serialized_messages = self.serialize_messages(messages)
            json.dump(serialized_messages, file, indent=4)

    # This function checks if the file exists. If it does not, it creates the file
    def check_file_exists(self, file_path: str):
        try:
            # Open the file and load the data.
            with open(file_path, "r") as file:
                # Load the data from the file.
                data = json.load(file)
                
                # Create a list of objects from the data. Loop through the data and create QA_Class objects.
                objects = []
                for message in data:
                    objects.append(QA_Class(message["question"], message["answer"], message["id"]))
                    
            return objects
        except:
            # If the file does not exist, first create the folders and then create the file. Return an empty list.
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                json.dump([], file)
                return []
    
    # This function serializes the messages to be saved in the json file.
    def serialize_messages(self, messages: list[QA_Class]):
        # Messages are a List of QA_Class objects. We need to serialize (convert them to a dict) them to save them in the json file.
        # Create a list of serialized messages. Loops through all the messages and creates a dictionary for each message.
        serialized_messages = []
        for message in messages:
            serialized_messages.append({
                "id": message.id,
                "question": message.question,
                "answer": message.answer
            })
        return serialized_messages
    
#endregion