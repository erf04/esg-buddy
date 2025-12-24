import os
from openai import AsyncOpenAI, RateLimitError, APIError, APIStatusError
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
        try:
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
                    error = run_status.last_error
                    if error and error.code == "rate_limit_exceeded":
                        # Create a proper rate limit error message
                        error_msg = error.message or "Rate limit exceeded"
                        error_body = error.body if hasattr(error, 'body') else None
                        logger.error(f"Rate limit error in send_message: {error_msg}")
                        
                        # Return a structured error instead of raising
                        return f"[RATE_LIMIT_ERROR] {error_msg}"
                    raise Exception(f"Assistant run failed: {error.message if error else 'Unknown error'}")
                await asyncio.sleep(0.5)

            # Fetch the messages (assistant's response)
            messages = await self.client.beta.threads.messages.list(
                order="desc", limit=1, thread_id=thread_id
            )

            if not messages.data:
                return ""

            latest = messages.data[0]
            return latest.content[0].text.value
            
        except Exception as e:
            # Check for rate limit in the exception
            error_str = str(e)
            if "rate_limit" in error_str.lower() or "429" in error_str:
                logger.error(f"Rate limit detected in send_message: {error_str}")
                return f"[RATE_LIMIT_ERROR] {error_str}"
            logger.error(f"Error in send_message: {error_str}")
            return f"[ERROR] {error_str}"

    async def stream_response(self, thread_id: str, content: str):
        try:
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
                elif event.event == "thread.run.failed":
                    error = event.data.last_error
                    if error and error.code == "rate_limit_exceeded":
                        error_msg = error.message or "Rate limit exceeded"
                        logger.error(f"Rate limit in stream: {error_msg}")
                        yield f"[RATE_LIMIT_ERROR] {error_msg}"
                    break
                    
        except Exception as e:
            error_str = str(e)
            # Check for rate limit in exception
            if "rate_limit" in error_str.lower() or "429" in error_str or "too many requests" in error_str.lower():
                logger.error(f"Rate limit detected in stream_response: {error_str}")
                yield f"[RATE_LIMIT_ERROR] {error_str}"
            else:
                logger.error(f"Error in stream_response: {error_str}")
                yield f"[ERROR] {error_str}"

    async def generate_esg_report_text(self, thread_id: str) -> str:
        logger.debug("Starting ESG report generation | thread_id=%s", thread_id)

        try:
            # 1. List existing messages
            messages = await self.client.beta.threads.messages.list(
                thread_id=thread_id,
                order="asc"
            )
            logger.debug("Existing messages count: %d", len(messages.data))

            esg_prompt = """
                Generate the full ESG report
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
                    
                    if error and error.code == "rate_limit_exceeded":
                        error_msg = error.message or "Rate limit exceeded"
                        logger.error(f"Rate limit in ESG generation: {error_msg}")
                        raise Exception(f"rate_limit_exceeded: {error_msg}")
                    
                    raise RuntimeError(
                        f"ESG generation failed: {error.code if error else 'Unknown'} - {error.message if error else 'Unknown error'}"
                    )

                await asyncio.sleep(0.8)

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
            return ""
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"Error in generate_esg_report_text: {error_str}")
            
            # Check if it's a rate limit error
            if "rate_limit" in error_str.lower() or "429" in error_str:
                logger.error(f"Rate limit in generate_esg_report_text: {error_str}")
                raise Exception(f"rate_limit_exceeded: {error_str}")
            
            raise