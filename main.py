from pathlib import Path

DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"


def search_documents(query):
    results = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(f"Could not read {file_path.name}: {error}")
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            if query.casefold() in line.casefold():
                results.append((file_path.name, line_number, line))

    return results


def main():
    DOCUMENTS_DIR.mkdir(exist_ok=True)

    print("\nWelcome to DocScout!")
    print("Search your text documents. Type 'quit' to exit.")

    while True:
        query = input("\nSearch: ").strip()

        if query.casefold() == "quit":
            print("Goodbye!")
            break

        if not query:
            print("Enter a word or phrase to search.")
            continue

        results = search_documents(query)

        if not results:
            print("No matches found.")
            continue

        print(f"\nFound {len(results)} matching lines:\n")

        for filename, line_number, line in results:
            print(f"{filename} — line {line_number}")
            print(f"  {line}\n")


if __name__ == "__main__":
    main()
