from query import generate_response


def main():

    print("Enterprise RAG Assistant")

    while True:

        query = input("\nEnter your query or if you want to exit, type 'exit'")

        if query.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = generate_response(query)

            print("\nResponse:")
            print(response)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()