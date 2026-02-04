import ollama
import json
import re
from sqlalchemy.orm import Session
from app.repositories.entry_repository import EntryRepository
from app.models.entry_model import Entry
from app.models.entry_request import EntryCreate

class EntryService:

#  Basiclly the processing time depends on 2 thing( 3 in your case ) :-
# 1. Input Length (The Read Speed) -> The more text you send, the more "Tokens" the AI has to read first. This is usually very fast, but if you sent a whole book, you would notice a small delay before it even starts thinking.

# 2. Output Length (The Writing Speed)-> The time it takes to see a response is mostly decided by how many words the AI writes.[the AI wrote a very short summary. It was likely faster ] , [ If In your Test 1, it wrote a more descriptive summary. That took longer, Because we forced it to return JSON, it has to be very careful with every { and ", which also adds a tiny bit of "thinking" time.]

# The "Cold Start" (Local Machine Special)-> Since you are running this on your own PC, the very first request is always the longest because Ollama has to "Wake up" the model and load all 4GB of Gemma into your RAM or Graphics Card (VRAM). Once it's "Warm," it responds much faster.

    def __init__(self):
        self.repo = EntryRepository() 

    def analyze_thought(self,content:str):
        # 1. The "job Description" for the AI
        system_prompt = """  
        You are the psychological analyst for the 'Reflecta' app.
        Analyze the user's raw thought and return ONLY a json object with:
        "sentiment": (One word : Happy , Anxious , Angry , or Neutral)
        "tasks":( A List of short actionable todos found in the text)
        "summary": (A one-sentence clean version of the thought)
        """

        # 2. Making the call to the Local Brain
        response = ollama.chat(model='gemma3:4b', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': content},
        ])

        # 3. Pulling the text out of the response
        return response['message']['content']

    def create_entry(self, db: Session, entry_data: EntryCreate) -> dict:
        # Step A: Save the raw "Mud" first 
        db_entry = Entry(raw_content=entry_data.raw_content)
        saved_entry = self.repo.save(db, db_entry)

        # Step B: Pass the mud through the "Sieve"
        ai_response_text = self.analyze_thought(entry_data.raw_content)
        
        # Default empty insights
        insights = {
            "sentiment": "Neutral",
            "summary": "Analysing..."
        }

        # Step C: Parse the AI Insight (JSON)
        try:
            json_match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
        except Exception as e:
            print(f"Error parsing AI JSON: {e}")

        # Step D: Return the merged data (Postman Receipt)
        return {
            "id": saved_entry.id,
            "raw_content": saved_entry.raw_content,
            "created_at": saved_entry.created_at,
            "sentiment": insights.get("sentiment"),
            "summary": insights.get("summary")
        }
