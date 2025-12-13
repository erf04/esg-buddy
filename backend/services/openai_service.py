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
        """
        Ask the AI to generate an ESG report as plain text
        """
        esg_prompt = """
        Based on our conversation about the company, please generate a comprehensive 
        ESG (Environmental, Social, Governance) report.
        
        Format it as a professional report with these sections:
        
        1. Executive Summary
        2. Environmental Performance
        3. Social Responsibility  
        4. Governance Structure
        5. Key Recommendations
        6. Conclusion
        
        Make it detailed, data-driven, and actionable. Use markdown formatting for headings.
        """
        
        # Send the prompt
        await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=esg_prompt
        )
        
        # Run the assistant
        run = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        
        # Wait for completion
        while True:
            run_status = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise Exception("ESG report generation failed")
        
        # Get the response
        messages = await self.client.beta.threads.messages.list(
            order="desc", limit=1, thread_id=thread_id
        )
        
        if not messages.data:
            raise Exception("No response from AI")
        
        latest = messages.data[0]
        return latest.content[0].text.value

