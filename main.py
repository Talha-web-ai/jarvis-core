import sys
from core.agent import JarvisAgent


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<goal>\"")
        return

    raw_goal = sys.argv[1]

    agent = JarvisAgent(
        raw_goal,
        fast_mode=True  # ⚡ CLI should be fast by default
    )

    result = agent.run()

    if result:
        print("\nFinal Answer:\n")
        print(result)
    else:
        print("\nNo meaningful output produced.")


if __name__ == "__main__":
    main()
