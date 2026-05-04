import argparse
import sys
from pathlib import Path


def cmd_ingest(_args):
    from src.threatlens.ingest import ingest
    ingest()


def cmd_ask(args):
    from src.threatlens.agent import ask
    result = ask(" ".join(args.question))
    print(f"\n{result['answer']}")
    if result["sources"]:
        print(f"\nSources: {', '.join(result['sources'])}")


def cmd_chat(_args):
    from src.threatlens.config import CHROMA_PATH
    if not Path(CHROMA_PATH).exists():
        print("No index found. Run 'python main.py ingest' first.")
        sys.exit(1)
    from src.threatlens.agent import ask, build_chain
    print("ThreatLens — interactive mode. Type 'exit' to quit.\n")
    chain = build_chain()
    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break
        if question.lower() in ("exit", "quit", "q"):
            break
        if not question:
            continue
        result = ask(question, chain=chain)
        print(f"\nThreatLens: {result['answer']}")
        if result["sources"]:
            print(f"Sources: {', '.join(result['sources'])}")
        print()


def main():
    parser = argparse.ArgumentParser(
        prog="threatlens",
        description="ThreatLens — local threat intelligence Q&A (powered by Ollama + LangChain)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest", help="Pull threat feeds and build vector index").set_defaults(func=cmd_ingest)

    p_ask = sub.add_parser("ask", help="Ask a single question and exit")
    p_ask.add_argument("question", nargs="+", help="The question to ask")
    p_ask.set_defaults(func=cmd_ask)

    sub.add_parser("chat", help="Start an interactive chat session").set_defaults(func=cmd_chat)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
