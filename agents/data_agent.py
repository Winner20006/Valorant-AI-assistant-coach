from agents.VLM import VLM
import PIL.Image

class DataAgent:
    def __init__(self):
        self.vlm = VLM()

    def fetch_data(self, query):
        """
        Fetches relevant game data based on the query.
        In a real implementation, this would pull data from the VLM or an external game API.
        """
        if "stats" in query.lower() or "performance" in query.lower():
            return "KDA: 12/8/5, Econ Rating: 4500, Combat Score: 280, Utility Usage: 85%"
        elif "round" in query.lower():
            return "Round 14: Won, Team Status: 3 alive, Enemy Status: 0 alive, Spike: Defused"
        
        return f'Simulated data for: {query}. VLM is analyzing the current frame.'