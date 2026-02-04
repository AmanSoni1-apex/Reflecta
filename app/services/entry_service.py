from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from app.repositories.entry_repository import EntryRepository
from app.models.entry_model import Entry
from app.models.entry_request import EntryCreate

import ollama
import json

class EntryService:

    def __init__(self):
        self.repo = EntryRepository() 

    def analyze_thought(self,content:str):
        # 1. The "job Description" for the AI
        system_prompt = """  
        You are the psychological analyst for the 'Reflecta' app.
        Analyze the user's raw thought and return ONLY a json object with 
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

    def create_entry(self, db: Session, entry_data: EntryCreate) -> Entry:
        # Step A: Save the raw "Mud" first 
        db_entry = Entry(raw_content=entry_data.raw_content)
        saved_entry = self.repo.save(db, db_entry)

        # Step B: Pass the mud through the "Sieve"
        ai_analysis = self.analyze_thought(entry_data.raw_content)

        # Step C: Print the insight to the terminal
        print(f"\n--- AI INSIGHT ---\n{ai_analysis}\n------------------\n")

        return saved_entry
