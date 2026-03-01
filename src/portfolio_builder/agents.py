"""Agents for the portfolio builder system using OpenAI Agent SDK."""

import json
from typing import Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class PortfolioBuilderAgents:
    def __init__(self):
        # Initialize OpenAI client - Note: OpenAI Assistant API is only available on OpenAI, not Gemini
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        else:
            raise ValueError("OPENAI_API_KEY environment variable is required for Assistant API functionality. "
                           "Note: The OpenAI Assistant API is not available on other platforms like Gemini.")

    def create_lead_strategist(self):
        """Create the Lead Strategist (Entry Agent) - Interviewer & Project Manager"""
        return self.client.beta.assistants.create(
            name="Portfolio Lead Strategist",
            description="Interviewer & Project Manager for portfolio building",
            model="gpt-4o",
            instructions="""
            You are the 'Portfolio Strategist' for the portfolio_builder system. Your goal is to extract high-impact data from the user through a natural conversation.

            Instructions:
            1. Interview Phase: Ask the user about their top 3 projects one by one. Do not move to the next project until you have: Project Name, Problem Solved, Tech Stack, and a Metric (e.g., 'saved 10 hours' or '100+ stars').
            2. Refinement: If the user is vague, suggest specific metrics they might have achieved.
            3. Handoff Trigger: Once you have data for 3 projects or the user says 'I'm done,' call the handoff_to_narrative_architect tool to pass the structured JSON data.
            4. Tone: Professional, inquisitive, and encouraging.
            """,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "handoff_to_narrative_architect",
                        "description": "Hand off to narrative architect with collected project data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "projects": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "Project name"},
                                            "problem": {"type": "string", "description": "Problem solved"},
                                            "tech_stack": {"type": "array", "items": {"type": "string"}},
                                            "metric": {"type": "string", "description": "Specific metric achieved"}
                                        },
                                        "required": ["name", "problem", "tech_stack", "metric"]
                                    }
                                }
                            },
                            "required": ["projects"]
                        }
                    }
                }
            ]
        )

    def create_narrative_architect(self):
        """Create the Narrative Architect (Processing Agent) - Content Writer & Storyteller"""
        return self.client.beta.assistants.create(
            name="Portfolio Narrative Architect",
            description="Content Writer & Storyteller for portfolio projects",
            model="gpt-4o",
            instructions="""
            You are a 'Senior Narrative Architect.' Your job is to transform the raw project data provided by the Strategist into a compelling professional story.

            Instructions:
            1. Headline Generation: Create a punchy, benefit-driven headline for the portfolio (e.g., 'Full-Stack Developer Specializing in Scalable AI').
            2. The STAR Method: Rewrite every project description using the Situation, Task, Action, and Result framework.
            3. Keyword Optimization: Seamlessly integrate relevant tech keywords (e.g., Python, React, AWS) for SEO and recruiter ATS.
            4. Handoff Trigger: Once the copy is polished, call handoff_to_visual_engineer to generate the final code.
            5. Tone: Confident, concise, and results-oriented.
            """,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "handoff_to_visual_engineer",
                        "description": "Hand off to visual engineer with polished copy",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "headline": {"type": "string", "description": "Professional headline"},
                                "projects": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "Project name"},
                                            "description": {"type": "string", "description": "STAR-formatted description"},
                                            "tech_stack": {"type": "array", "items": {"type": "string"}},
                                            "metric": {"type": "string", "description": "Specific metric achieved"}
                                        },
                                        "required": ["name", "description", "tech_stack", "metric"]
                                    }
                                },
                                "bio": {"type": "string", "description": "Professional bio"}
                            },
                            "required": ["headline", "projects", "bio"]
                        }
                    }
                }
            ]
        )

    def create_visual_engineer(self):
        """Create the Visual Engineer (Output Agent) - Frontend Developer"""
        return self.client.beta.assistants.create(
            name="Portfolio Visual Engineer",
            description="Frontend Developer creating portfolio websites",
            model="gpt-4o",
            instructions="""
            You are the 'Visual Engineer.' Your sole task is to take the polished copy and turn it into a production-ready, single-page portfolio.

            Instructions:
            1. Design System: Use a modern 'Bento Box' or 'Minimalist Dark Mode' layout using Tailwind CSS.
            2. Accessibility: Ensure all images have alt text placeholders and the site is fully responsive (mobile-first).
            3. Code Quality: Provide a single, valid HTML file (including CDN links for Tailwind/Lucide icons). Use clean, semantic HTML5.
            4. CTA: Ensure the 'Contact Me' or 'Resume Download' button is the most prominent element.
            5. Output: Provide the full code block and instructions on how to run it.
            """
        )


def run_portfolio_builder():
    """Main function to run the portfolio builder with handoffs"""
    agents = PortfolioBuilderAgents()

    # Create assistants for each agent
    strategist = agents.create_lead_strategist()
    architect = agents.create_narrative_architect()
    engineer = agents.create_visual_engineer()

    print("🚀 Portfolio Builder started! I'm your Lead Strategist.")
    print("I'll help you build an impressive portfolio by collecting information about your projects.")
    print("\nLet's start with your first project. What's the name of your most significant project?")

    # Create initial thread
    thread = agents.client.beta.threads.create()

    # Add initial message to start the conversation
    agents.client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="I'm ready to build my portfolio. Let's start with my projects."
    )

    current_assistant = strategist
    agent_name = "Lead Strategist"

    while True:
        # Run the current agent
        run = agents.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=current_assistant.id
        )

        # Process the run once it's completed
        if run.status == "completed":
            messages = agents.client.beta.threads.messages.list(
                thread_id=thread.id
            )

            # Get the latest message
            latest_message = None
            for msg in messages:
                if msg.role == "assistant":
                    latest_message = msg
                    break

            if latest_message:
                response_text = ""
                for content_block in latest_message.content:
                    if content_block.type == "text":
                        response_text += content_block.text.value

                print(f"\n[{agent_name}] Assistant: {response_text}")

            # Check for tool calls
            run_steps = agents.client.beta.threads.runs.steps.list(
                thread_id=thread.id,
                run_id=run.id
            )

            tool_called = False
            for step in run_steps:
                if step.step_details.type == "tool_calls":
                    for tool_call in step.step_details.tool_calls:
                        if tool_call.function.name == "handoff_to_narrative_architect":
                            print(f"\n[🔄 HANDOFF] Moving to Narrative Architect...")

                            # Parse the arguments
                            projects_data = json.loads(tool_call.function.arguments)

                            # Create message for next agent
                            next_message = f"I've collected the following project data: {json.dumps(projects_data, indent=2)}. Please transform this into compelling copy using the STAR method, optimize for SEO and ATS systems, and create a professional headline and bio."

                            # Add message to thread for next agent
                            agents.client.beta.threads.messages.create(
                                thread_id=thread.id,
                                role="user",
                                content=next_message
                            )

                            # Switch to architect agent
                            current_assistant = architect
                            agent_name = "Narrative Architect"
                            tool_called = True
                            break

                        elif tool_call.function.name == "handoff_to_visual_engineer":
                            print(f"\n[🔄 HANDOFF] Moving to Visual Engineer...")

                            # Parse the arguments
                            copy_data = json.loads(tool_call.function.arguments)

                            # Create message for next agent
                            next_message = f"I've prepared the following copy: {json.dumps(copy_data, indent=2)}. Please create a stunning portfolio website with modern 'Bento Box' or 'Minimalist Dark Mode' design using Tailwind CSS. Generate complete HTML code."

                            # Add message to thread for next agent
                            agents.client.beta.threads.messages.create(
                                thread_id=thread.id,
                                role="user",
                                content=next_message
                            )

                            # Switch to engineer agent
                            current_assistant = engineer
                            agent_name = "Visual Engineer"
                            tool_called = True
                            break

                    if tool_called:
                        break

            if not tool_called:
                # If no tool was called and we're at the final agent, we're done
                if current_assistant.id == engineer.id:
                    print("\n✅ Portfolio creation complete! Your portfolio has been generated.")
                    break
                else:
                    # Get user input for next iteration
                    user_input = input(f"\n[{agent_name}] User: ")

                    if user_input.lower() in ["quit", "exit", "done"]:
                        print("\n👋 Thank you for using Portfolio Builder!")
                        break

                    # Add user message to thread
                    agents.client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=user_input
                    )

        elif run.status == "failed":
            print(f"\n❌ Error: {run.last_error}")
            break

    # Clean up assistants
    agents.client.beta.assistants.delete(strategist.id)
    agents.client.beta.assistants.delete(architect.id)
    agents.client.beta.assistants.delete(engineer.id)


if __name__ == "__main__":
    run_portfolio_builder()