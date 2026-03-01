<<<<<<< HEAD
# portfolio_builder
=======
# Portfolio Builder

An AI-powered portfolio builder using OpenAI Agent SDK with handoff architecture. This tool uses three specialized AI agents to create impressive portfolios:

1. **Lead Strategist** - Interviews you about your projects
2. **Narrative Architect** - Crafts compelling stories using the STAR method
3. **Visual Engineer** - Creates stunning portfolio websites

## Architecture

The system implements a handoff architecture with three distinct personas:

### 1. The Lead Strategist (Entry Agent)
- Role: Interviewer & Project Manager
- System Prompt: Extracts high-impact data through natural conversation
- Asks about top 3 projects (Name, Problem Solved, Tech Stack, Metrics)
- Hands off to copywriter when complete

### 2. The Narrative Architect (Processing Agent)
- Role: Content Writer & Storyteller
- Transforms raw project data into compelling professional stories
- Uses STAR method (Situation, Task, Action, Result)
- Optimizes for SEO and recruiter ATS systems
- Hands off to designer when copy is polished

### 3. The Visual Engineer (Output Agent)
- Role: Frontend Designer & Developer
- Creates production-ready, single-page portfolios
- Uses modern 'Bento Box' or 'Minimalist Dark Mode' layouts
- Ensures accessibility and mobile responsiveness
- Generates complete HTML with Tailwind CSS

## Setup

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **Note**: This system uses the OpenAI Assistant API which is only available through OpenAI's platform.
   Alternative providers like Google Gemini do not currently support the Assistant API functionality.

## Usage

Run the portfolio builder:
```bash
python -m src.portfolio_builder.main
```

Or using the installed script:
```bash
portfolio-builder
```

## Features

- Three-tier AI agent system for comprehensive portfolio creation
- Natural conversation flow for easy project collection
- STAR method storytelling for impactful project descriptions
- Modern, responsive portfolio designs
- SEO and ATS optimization
- Accessible markup with proper alt texts

## Requirements

- Python 3.12+
- API key from OpenAI or compatible provider
- Internet connection for API calls
>>>>>>> cbcc65d (feat: Implement initial scaffolding)
