# main.py
import argparse
import pandas as pd
from similarity_engine import SimilarityEngine

def main():
    # CLI arguments
    parser = argparse.ArgumentParser(description="Ticket Similarity Demo")
    parser.add_argument("--tickets_file", type=str, default="tickets.csv", help="Path to tickets CSV file")
    parser.add_argument("--query_index", type=int, default=None, help="Index of the ticket to compare others against")
    parser.add_argument("--top_k", type=int, default=10, help="Number of top results to return after pre-filtering")
    parser.add_argument("--final_n_filter", type=int, default=5, help="Number of results after semantic similarity")
    args = parser.parse_args()

    # Load tickets
    tickets = pd.read_csv(args.tickets_file)

    # If query index not given, let user pick interactively
    if args.query_index is None:
        print("\n📋 Available Tickets (showing first 15):\n")
        for i, row in tickets.head(15).iterrows():
            print(f"Index {i}: [ID {row['Issue Key']}] {row['Summary'][:80]}")

        while True:
            try:
                query_index = int(input(f"\nEnter query index (0 to {len(tickets)-1}): "))
                if 0 <= query_index < len(tickets):
                    break
                else:
                    print("❌ Invalid index. Try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    else:
        query_index = args.query_index
        if query_index < 0 or query_index >= len(tickets):
            raise ValueError(f"Invalid query_index: {query_index}. Must be between 0 and {len(tickets)-1}.")

    # Pick query ticket
    query_ticket = tickets.iloc[query_index]
    print(f"\n🔍 Query Ticket (index {query_index}):")
    print(f"Issue Key: {query_ticket['Issue Key']}")
    print(f"Summary: {query_ticket['Summary']}")
    print(f"Description: {query_ticket['Description']}\n")

    # Run similarity engine
    engine = SimilarityEngine(tickets)
    similar_tickets = engine.find_similar(
        query_index=query_index,
        top_k=args.top_k,
        final_n_filter=args.final_n_filter
    )

    # Show results
    print(f"✅ Top {args.final_n_filter} similar tickets:\n")
    for idx, row in similar_tickets.iterrows():
        print(f"[{row['Issue Key']}] {row['Summary']} (score={row['score']:.4f})")

if __name__ == "__main__":
    main()
