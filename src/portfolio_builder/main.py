
from .agents import run_portfolio_builder
import os
from dotenv import load_dotenv

def main():
    """Main entry point for the portfolio builder."""
    load_dotenv()

    print("🚀 Welcome to the Portfolio Builder!")
    print("This tool will help you create an impressive portfolio using AI agents.")
    print("="*70)

    # Run the portfolio builder
    run_portfolio_builder()


if __name__ == "__main__":
    main()
