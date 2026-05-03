import argparse
import sys


def _check_api_key():
    from src.threatlens.config import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is not set. Copy .env.example to .env and add your key.")
        sys.exit(1)


def cmd_ingest(args):
    from src.threatlens.ingest import ingest
    ingest(args.path)


def cmd_ask(args):
    from src.threatlens.agent import ask
    result = ask(" ".join(args.question))
    print(f"\n{result['answer']}")
    if result["sources"]:
        print(f"\nSources: {', '.join(result['sources'])}")


def cmd_chat(_args):
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
    _check_api_key()

    parser = argparse.ArgumentParser(
        prog="threatlens",
        description="ThreatLens — LangChain-powered threat intelligence Q&A agent",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Ingest documents into the vector store")
    p_ingest.add_argument("--path", default=None, help="Directory to ingest (default: ./data)")
    p_ingest.set_defaults(func=cmd_ingest)

    p_ask = sub.add_parser("ask", help="Ask a single question and exit")
    p_ask.add_argument("question", nargs="+", help="The question to ask")
    p_ask.set_defaults(func=cmd_ask)

    p_chat = sub.add_parser("chat", help="Start an interactive chat session")
    p_chat.set_defaults(func=cmd_chat)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
