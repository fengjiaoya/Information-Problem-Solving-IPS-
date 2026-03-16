# IPS Research & Experiment Platform

## 📌 Project Overview
[cite_start]This platform is a specialized Web application designed to investigate **Information Problem Solving (IPS)** and **Self-Regulated Learning (SRL)** in online environments[cite: 1, 9, 462, 471]. [cite_start]Using the **SR-ISPS model** as an analytic framework, the tool captures how learners iterate between **Problem Representation (PR)** and **Solution Generation (SG)** when tackling ill-structured tasks[cite: 511, 512, 1118, 1119].

## 🧪 Theoretical Framework
[cite_start]The platform is built to identify and record specific cognitive and metacognitive behaviors[cite: 11, 203, 814]:
* [cite_start]**I (Instruction)**: Orientation and task-definition behaviors[cite: 610, 1121].
* [cite_start]**Q (Query)**: Information-seeking intent and problem re-representation[cite: 610, 1123].
* [cite_start]**P (Processing)**: Information evaluation and reading of AI-generated content[cite: 610, 1123].
* [cite_start]**W (Writing)**: Solution implementation and knowledge integration[cite: 610, 1123].

## 🛠️ Core Features
* **Split-Screen Interface**: A dual-column layout with the **Dynamic Notebook** on the left (Solution Generation) and the **AI Assistant** on the right (Problem Representation).
* **High-Fidelity Logging**: Every interaction is timestamped and saved to a CSV file (`comprehensive_research_log.csv`), recording action types, content snapshots, and writing progress (note length).
* [cite_start]**Scaffolded AI Interaction**: Integrated System Prompts restrict the AI to an "Educational Tutor" mode, providing qualitative feedback rather than direct answers to encourage deep processing[cite: 14, 95, 386].
* **Persistence**: Uses Streamlit `session_state` to maintain the experiment context across user interactions.

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* OpenAI API Key

### Installation
1.  Clone this repository to your local machine (e.g., your `UNT System\...\Code` directory).
2.  Install the required libraries:
    ```bash
    pip install streamlit openai pandas
    ```

### Running the Experiment
1.  Navigate to the project folder in your terminal.
2.  Execute the following command:
    ```bash
    streamlit run app.py
    ```
3.  The platform will automatically open in your default browser (typically at `localhost:8501`).

## 📊 Data Output
[cite_start]The platform generates a `comprehensive_research_log.csv` file structured for **Lag Sequential Analysis (LSA)**[cite: 614, 615]. Data includes:
* `timestamp`: Precision timing for **Time-on-Task** analysis.
* `action_type`: Coded identifiers for behavioral transitions ($I, Q, P, W, F$).
* [cite_start]`content_snapshot`: Text data for qualitative triangulation[cite: 193, 619, 1182].
* `current_note_length`: Quantitative measure of writing productivity.

## ⚖️ License
This project is developed for academic research purposes.
