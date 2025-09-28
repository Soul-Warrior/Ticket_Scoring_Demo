# 🔍 JIRA AI Ticket Scoring Demo (Proof of Concept)

This project serves as a **Proof of Concept (PoC) demo** for a system that automatically finds the most semantically similar past JIRA tickets to a newly assigned ticket.

**The primary goal of this demo is to showcase the core logic: combining traditional TF-IDF filtering with advanced semantic similarity for highly accurate results.**

## 🌟 Demo Functionality (What This Repository Does)

This repository demonstrates the core ticket matching logic on local data:

1.  **Load Data:** Reads JIRA ticket data (Issue Key, Summary, Description) from the included **`tickets.csv`** file.
2.  **Query Selection:** Prompts the user to input the index of a ticket from the loaded data to use as the "newly assigned ticket" (the query).
3.  **Two-Stage Matching:**
    * **Pre-Filter (Speed):** Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** on the titles and descriptions to quickly filter down the massive list of tickets to the top k most textually similar candidates.
    * **Semantic Matching (Accuracy):** Applies a pre-trained **Sentence Transformer model** to calculate the cosine similarity between the query ticket and the candidates, providing a high-quality ranking.
4.  **Output:** Prints the top N most similar tickets.

---

## 🚀 Getting Started

Follow these steps to run the similarity demo locally.

### Prerequisites

* **Python 3.9+**
* `pip` package manager

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Soul-Warrior/Ticket_Scoring_Demo.git](https://github.com/Soul-Warrior/Ticket_Scoring_Demo.git)
    cd Ticket_Scoring_Demo
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(This file contains necessary packages like `sentence-transformers`, `scikit-learn`, `numpy`, and `pandas`.)*

### Usage

Run the main script using the default settings or customize the execution with optional arguments.

#### 1. Default (Interactive) Usage

If no arguments are provided, the script uses the default settings and prompts for the query index:

```bash
python demo.py
```

#### 2. Usage with Optional Arguments

You can bypass the interactive prompt and customize the filtering steps using the following optional arguments defined in `run_demo.py`:

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--tickets_file` | `str` | `"tickets.csv"` | Path to the input CSV file containing JIRA tickets. |
| `--query_index` | `int` | `None` | Index of the ticket to compare others against (skips interactive prompt). |
| `--top_k` | `int` | `10` | Number of top results to return *after* **TF-IDF pre-filtering**. |
| `--final_n_filter` | `int` | `5` | Number of final results to return *after* **semantic similarity** scoring. |

**Example**: Run a non-interactive search on the ticket at index 50, pre-filter to 20 candidates, and show the final top 3 matches:

```bash
python run_demo.py --tickets_file tickets.csv --query_index 50 --top_k 20 --final_n_filter 3
```
---
## 🏗️ Actual Project Architecture (Production Use Case) 

This demo is based on a planned production system designed for real-time user assistance. 
| Component | Technology/Trigger | Function | 
| :--- | :--- | :--- | 
| **Data Ingestion** | Cron Job (Daily) | Queries the JIRA API for all tickets and saves data to a secure database/storage for retrieval. | 
| **Trigger** | JIRA Webhook | JIRA sends an HTTP POST request to our system **immediately** upon a ticket being assigned to a user. The payload includes the new issue key, user name, and **user email**. | 
| **Matching Engine** | Core Logic (This Demo) | Executes the two-stage similarity process (TF-IDF + Semantic AI) on the new ticket against the entire historical dataset. | 
| **User Notification** | Email Service (e.g., SendGrid) | Automatically sends an email to the assigned user (using the email from the webhook) with the list of N most matching tickets for reference. |

### Why the Two-Stage Approach? 
1. **TF-IDF Pre-filter:** Dramatically reduces the number of tickets that need heavy AI processing, **saving time and computational cost** when dealing with thousands of tickets. 
2. **Semantic Similarity:** Ensures the matches are based on the **meaning and intent** of the ticket, not just keyword overlap, providing much higher relevance. 
---