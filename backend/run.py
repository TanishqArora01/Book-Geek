"""Entry point for BookGeek-AI."""

import argparse
import sys

import uvicorn


def main():
    """Start the BookGeek-AI server."""
    parser = argparse.ArgumentParser(description="BookGeek-AI Server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--prod", action="store_true")

    args = parser.parse_args()

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=not args.prod,
        log_level="info",
    )


if __name__ == "__main__":
    main()
