import os
import sys
from google import genai

# Check for API key
if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Run: export GEMINI_API_KEY='your_key'")
    sys.exit(1)

# Initialize client and create a persistent chat session
client = genai.Client()
chat = client.chats.create(model="gemini-2.5-flash")

print("==================================================")
print("   AI Assistant with Memory (Type 'exit' to quit) ")
print("==================================================")

while True:
    try:
        user_prompt = input("\nYou: ")
        if user_prompt.strip().lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_prompt.strip():
            continue

        print("\nAI is thinking...")
        
        # Send message within the chat session to preserve context
        response = chat.send_message(user_prompt)
        
        print(f"\nAI Assistant:\n{response.text}")
        print("-" * 50)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        break