from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import openai
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


book_search_path = Path(__file__).parent / "book_search.py"

client = MultiServerMCPClient(
    {   
        "book_search": {
            "command": "python",
            "args": [str(Path(__file__).parent / "book_search.py")],
            "transport": "stdio",
        },
        "apify": {
            "transport": "sse",
            "url": "https://mcp.apify.com/sse?actors=runtime/goodreads-book-scraper",
            "headers": {
                "Authorization": f"Bearer {os.getenv('APIFY_API_KEY')}",
            }
        }
    }
)


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

async def chat():
    llm = ChatOpenAI(name="o4-mini", top_p=0.5, api_key=openai.api_key)
    tools = await client.get_tools()
    agent = create_react_agent(
        model=llm,
        tools = tools,
        checkpointer= InMemorySaver(),
        prompt="You are an agent that helps users find books based on their connections." \
        "You can use tools to search for information about books." \
        "Consider short books to be books that are no longer than 130 pages." \
        "Consider long books to be books that are longer than 400 pages." \
        "When answering, choose the 5 best books based on user reviews." \
        "To find information about a specific book, pass the name in English, as the user wrote it and in UTF-8 encoding, to the name search tool." \
        "If the user is searching for books with a specific term, use the goodreads-book-scraper tool from apify and pass the search term in English." 
    )

    print("Enter your request (e.g. 'I want a short novel'). Use /q to exit.\n")

    while True:
            # try:
        user_input = input("> ")

        if user_input.lower() == "/q":
            print("Quitting...")
            break

        config = {
            "configurable": {
                "thread_id": "1"
            }
            }

        # response = await agent.ainvoke(
        #     {"messages": [{"role": "user", "content": user_input}]}, config=config,
        # )

        async for chunk in agent.astream(
                        {"messages": user_input},
                        stream_mode=["messages", "custom"],
                        config=config,
                    ):
            print(chunk)
            import pdb
            pdb.set_trace()
        print("\nAgent response:\n")
        # print(response["messages"][-1].content)
        print("\n")
            # except: 
            #      print(f"Ocorreu um erro: {e}")
            #break

if __name__ == "__main__":
    asyncio.run(chat())