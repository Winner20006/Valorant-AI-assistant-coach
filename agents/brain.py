from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import json
from agents.mid_game import MidGameAgent
from agents.post_game import PostGameAgent
from agents.data_agent import DataAgent

class Brain:
    def __init__(self, model="llama3.2:1b", temperature=0):
        self.llm = Ollama(model=model, temperature=temperature)
        self.mid_game_agent = MidGameAgent(model=model, temperature=temperature)
        self.post_game_agent = PostGameAgent(model=model, temperature=temperature)
        self.data_agent = DataAgent()

        self.router_prompt = PromptTemplate(
            input_variables=["input"],
            template="""
Task: Classify the VALORANT question.

"agent": 
- "mid_game" if it's about what to do RIGHT NOW in a round.
- "post_game" if it's about what happened in the PAST or a general claim.

"needs_data":
- true if it needs live round data.
- false otherwise.

Input: {input}

Return ONLY JSON: {{"agent": "...", "needs_data": ...}}
"""
        )
        # Chain (LCEL) with improved parsing
        self.router_chain = self.router_prompt | self.llm | JsonOutputParser()

    def route(self, user_input):
        try:
            return self.router_chain.invoke({"input": user_input})
        except Exception:
            # Fallback logic if JSON parsing fails
            return {"agent": "mid_game", "needs_data": True}

    def ask(self, user_input):
        route_info = self.route(user_input)
        
        data = None
        if route_info.get('needs_data', False):
            # If data is needed, we go to the data agent and come back with the data
            data = self.data_agent.fetch_data(user_input)
            
        if route_info.get('agent') == 'mid_game':
            # For mid-game, we use the fetched data as round_data
            round_data = data if data else "No live data available."
            return self.mid_game_agent.ask(round_data=round_data, question=user_input)
        else:
            # For post-game, we currently just pass the claim
            # If data was fetched, we could potentially append it, but the current PostGameAgent takes only 'claim'
            return self.post_game_agent.ask(claim=user_input)

    def handle_event(self, event_type):
        """
        Handles autonomous events detected by the VLM.
        """
        if event_type == "round_ended":
            # Feedback about the game
            return self.post_game_agent.ask("The round has ended. Provide a brief, constructive feedback about the game performance and suggest improvements for the next round.")
        
        elif event_type == "player_killed_enemy":
            # Good job + snapshot of stats
            stats = self.data_agent.fetch_data("current performance snapshot")
            return f"Good job on that kill! Here is a quick snapshot of your current game state: {stats}"
        
        elif event_type == "player_died":
            # Good game + round stats
            stats = self.data_agent.fetch_data("round end statistics")
            return f"Good game. You had a solid effort. Here are your stats for the round: {stats}"
        
        return None







