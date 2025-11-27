import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

    async def create_thread(self):
        thread = await self.client.beta.threads.create()
        return thread.id

    async def send_message(self, thread_id: str, content: str) -> str:
        # Create user message
        await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )

        # Run the assistant
        run = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )

        # Wait for the run to complete
        while True:
            run_status = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise Exception("Assistant run failed")

        # Fetch the messages (assistant's response)
        messages = await self.client.beta.threads.messages.list(
            order="desc", limit=1, thread_id=thread_id
        )

        if not messages.data:
            return "No response found"

        latest = messages.data[0]
        return latest.content[0].text.value
