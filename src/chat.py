from google.genai import errors


def start_chat():
    """
    Starts a terminal chat session
    """
    from .config import chat
    print(
        """
        --- Gemini 2.5 flash ---
        <list things user can ask>
        """
    )
    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() == "exit":
                break

            if not user_input.strip():
                continue

            response = chat.send_message(user_input)
            print(f"\nGemini: {response.text}\n")

        except errors.APIError as e:
            # This catches specific Google API errors (Rate limits, invalid key, blocked content)
            print(f"\n[Gemini API Error]: {e.message} (Status Code: {e.code})")
            if e.code == 429:
                print("-> You've hit the free tier rate limit. Please wait a moment before trying again.\n")
            elif e.code == 403:
                print("-> Authentication error. Please check your GOOGLE_API_KEY.\n")

        except Exception as e:
            # This catches unexpected errors (like local network disconnects)
            print(f"\n[System Error]: An unexpected error occurred: {e}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
