import logging
import sys
import json
import time
from stt.stt_model import STT
from agents.brain import Brain
from tts.tts_model import TTS
from agents.VLM import VLM
from PIL import ImageGrab

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("--- Sky Final: VALORANT Decision Support AI ---")
    
    # Initialize components
    try:
        stt = STT()
        brain = Brain()
        vlm = VLM()
        # TTS might fail if model files are missing, let's handle it gracefully
        try:
            tts = TTS()
        except FileNotFoundError:
            logger.warning("TTS model files not found. Speech output will be disabled.")
            tts = None
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        sys.exit(1)

    print("\n✅ System ready. Sky is listening for your questions or watching for game events.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            # 1. Listen (STT) - non-blocking with a short timeout
            # This allows the AI to respond when the player calls it.
            user_text = stt.listen(timeout=0.5)
            
            if user_text:
                print(f"\n👤 User: {user_text}")
                
                # 2. Process (Brain)
                print("🧠 Thinking...")
                response = brain.ask(user_text)
                
                print(f"🤖 Sky: {response}")
                
                # 3. Speak (TTS)
                if tts:
                    tts.speak(response)
                
                continue # Skip VLM check for this iteration after interaction

            # 4. Watch (VLM) for autonomous events
            try:
                # Capture the screen
                screenshot = ImageGrab.grab()
                
                # Detect events using the VLM
                events_json = vlm.detect_events(image_obj=screenshot)
                events = json.loads(events_json)
                
                # Check if any event occurred
                for event_type, occurred in events.items():
                    if occurred:
                        print(f"\n🔔 Event detected: {event_type}")
                        
                        # Get appropriate response for the event
                        response = brain.handle_event(event_type)
                        
                        if response:
                            print(f"🤖 Sky: {response}")
                            if tts:
                                tts.speak(response)
                        
                        # Delay to prevent multiple triggers for the same event
                        time.sleep(5)
                        break # Process one event at a time
                        
            except Exception as e:
                # Silently catch screen capture errors to keep the loop alive
                pass
            
    except KeyboardInterrupt:
        print("\n👋 Exiting Sky Final. Good luck in your games!")

if __name__ == "__main__":
    main()
