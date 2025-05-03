import os
from dotenv import load_dotenv

# LLM imports
import asyncio
from langchain_groq import ChatGroq

# MCP imports
from mcp_use import MCPAgent, MCPClient


async def run_memory_chat():
    """
    Run a chat using MCPAgent's built-in conversation memory.
    """

    # Load the environment variables
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Config file path
    config_file = "server/weather.json"

    print("Initializing MCPAgent chat with memory...")

    # Create MCPClient and MCPAgent with memory enabled
    client = MCPClient(config=config_file)
    llm = ChatGroq(model="qwen-qwq-32b")

    # Create MCPAgent with memory=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=5,
        memory_enabled=True,  # Enable memory built-in conversation memory
    )

    print("=======================================================")
    print("MCPAgent initialized. Starting chat...")
    print("You can start chatting with the agent. Type 'exit' to quit.")
    print("Type 'clear' to clear the conversation history.")
    print("=======================================================")

    try:
        # Main chat loop
        while True:
            user_input = input("You: ")

            # Check for exit command
            if user_input.lower() == "exit":
                print("Exiting chat...")
                break

            # Check for clear command
            elif user_input.lower() == "clear":
                agent.clear_memory()
                print("Conversation history cleared.")
                continue

            # Get the agent's response
            print("\nAgent: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"Error: {e}")
                print("Please try again.")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()
        print("All sessions closed.")


if __name__ == "__main__":
    # Run the chat in an asyncio event loop
    asyncio.run(run_memory_chat())

# This code is a simple chat client that uses the MCPAgent class to interact with a language model.
# It allows the user to chat with the agent, clear the conversation history, and exit the chat.
# The agent uses the Groq API for language processing and can handle multiple sessions.
# The code is designed to be run in an asynchronous environment, using asyncio for concurrency.
# The MCPClient class is used to manage the connection to the Groq API and handle sessions.
# The agent's memory is enabled by default, allowing it to remember previous interactions.
# The user can clear the memory at any time by typing 'clear'.
# The code is structured to handle exceptions gracefully and ensure that all sessions are closed properly.
# The agent's responses are printed to the console, and the user can interact with it in real-time.
