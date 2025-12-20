import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import logging

logger = logging.getLogger(__name__)

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
    
    async def stream_response(self, thread_id: str, content: str):
        # Create user message
        await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )

        # Create run with streaming enabled
        stream = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            stream=True
        )

        async for event in stream:
            if event.event == "thread.message.delta":
                if hasattr(event.data, 'delta') and hasattr(event.data.delta, 'content'):
                    for content_block in event.data.delta.content:
                        if content_block.type == "text" and hasattr(content_block.text, 'value'):
                            yield content_block.text.value
            elif event.event == "thread.run.completed":
                break


    async def generate_esg_report_text(self, thread_id: str) -> str:
        logger.debug("Starting ESG report generation | thread_id=%s", thread_id)

        # 1. List existing messages
        messages = await self.client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc"
        )
        logger.debug("Existing messages count: %d", len(messages.data))

        esg_prompt = """
        Based on our conversation about the company, please generate a comprehensive 
        ESG report.
        """

        # 2. Send prompt
        logger.debug("Sending ESG prompt to thread")
        await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=esg_prompt
        )

        # 3. Run assistant
        run = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )
        logger.debug("Run created | run_id=%s", run.id)

        # 4. Poll status (WITH sleep)
        while True:
            run_status = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            logger.debug(
                "Run status | run_id=%s | status=%s",
                run.id,
                run_status.status
            )

            if run_status.status == "completed":
                break

            if run_status.status == "failed":
                error = run_status.last_error
                logger.error(
                    "Run failed | code=%s | message=%s",
                    getattr(error, "code", None),
                    getattr(error, "message", None),
                )
                raise RuntimeError(
                    f"ESG generation failed: {error.code} - {error.message}"
                )

            await asyncio.sleep(0.8)  # VERY IMPORTANT

        # 5. Fetch latest assistant message
        messages = await self.client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            limit=5
        )

        logger.debug("Fetched %d messages after completion", len(messages.data))

        # 6. Find the assistant response safely
        for msg in messages.data:
            if msg.role == "assistant":
                for block in msg.content:
                    if block.type == "text":
                        logger.debug("Assistant response found")
                        return block.text.value

        logger.error("No assistant text response found")
        raise RuntimeError("No valid text response from assistant")

