import requests
import ollama
import json
import os
import re # re -> regular expression AI models are "chatty." Even if you ask for JSON, they often add extra words like "Sure, here it is..." which breaks our code , re module acts like a JSON Magnet. It scans a big pile of messy text, ignores the talkative noise, and "extracts" only the part between { and }.
from sqlalchemy.orm import Session
from app.repositories.entry_repository import EntryRepository
from app.models.entry_model import Entry
from app.models.entry_request import EntryCreate
from openai import OpenAI 
class EntryService:

#  Basiclly the processing time depends on 2 thing( 3 in your case ) :-
# 1. Input Length (The Read Speed) -> The more text you send, the more "Tokens" the AI has to read first. This is usually very fast, but if you sent a whole book, you would notice a small delay before it even starts thinking.

# 2. Output Length (The Writing Speed)-> The time it takes to see a response is mostly decided by how many words the AI writes.[the AI wrote a very short summary. It was likely faster ] , [ If In your Test 1, it wrote a more descriptive summary. That took longer, Because we forced it to return JSON, it has to be very careful with every { and ", which also adds a tiny bit of "thinking" time.]

# The "Cold Start" (Local Machine Special)-> Since you are running this on your own PC, the very first request is always the longest because Ollama has to "Wake up" the model and load all 4GB of Gemma into your RAM or Graphics Card (VRAM). Once it's "Warm," it responds much faster.

    def __init__(self):
        self.repo = EntryRepository() 

    def analyze_thought(self, content: str) -> str:
        # 1. Preparing the "Sieve" (Prompt)
        system_prompt = """  
        You are the psychological analyst for the 'Reflecta' app.
        Analyze the user's raw thought and return ONLY a json object with:
        "sentiment": (One word : Happy , Anxious , Angry , or Neutral)
        "tasks":( A List of short actionable todos found in the text)
        "summary": (A one-sentence clean version of the thought)
        """

        api_url="https://openrouter.ai/api/v1/chat/completions"
        header={
            "Authorization": "Bearer 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"
        }
        payload={
            "model":"alibaba/tongyi-deepresearch-30b-a3b",
            "temprature":0,
            "messages":[
                {'role':'system' ,'content':system_prompt},
                {'role':'user' ,'content':content}
            ]
        }
        response=requests.post(api_url,headers=header,json=payload)
        data=response.json()
        return data['choices'][0]['message']['content']

    def create_entry(self, db: Session, entry_data: EntryCreate, user_id: int) -> dict:
        # Step A: Pass the mud through the "Sieve" FIRST (So we can save the results)
        ai_response_text = self.analyze_thought(entry_data.raw_content)
        
        # Default empty insights
        insights = {
            "sentiment": "Neutral",
            "summary": "Analysing..."
        }

        # Step B: Parse the AI Insight (JSON)
        try:
            json_match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
        except Exception as e:
            print(f"Error parsing AI JSON: {e}")

        # Step C: Save the raw "Mud" AND the "Insights" to the DB
        db_entry = Entry(
            raw_content=entry_data.raw_content,
            sentiment=insights.get("sentiment"),
            summary=insights.get("summary"),
            user_id=user_id
        )
        saved_entry = self.repo.save(db, db_entry)

        # Step D: Return the merged data (Postman Receipt)
        return {
            "id": saved_entry.id,
            "raw_content": saved_entry.raw_content,
            "created_at": saved_entry.created_at,
            "sentiment": saved_entry.sentiment,
            "summary": saved_entry.summary
        }

    def get_all_entries(self, db: Session, user_id: int) -> list[Entry]:
        return self.repo.get_all(db, user_id)

    def delete_entry(self, db: Session, entry_id: int, user_id: int):
        entry = self.repo.get_by_id(db, entry_id, user_id)
        if not entry:
            return None
        self.repo.delete(db, entry)
        return True
