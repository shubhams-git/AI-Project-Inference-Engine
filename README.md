README.md

# Inference Engine

This project implements an inference engine for propositional logic using various methods such as Forward Chaining, Backward Chaining, Truth Table, and Resolution Prover. The engine can be used to determine if a query can be inferred from a given knowledge base.

## Table of Contents

- [Overview](#overview)
- [Frameworks and Languages](#frameworks-and-languages)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Inference Methods](#inference-methods)
  - [Forward Chaining (FC)](#forward-chaining-fc)
  - [Backward Chaining (BC)](#backward-chaining-bc)
  - [Truth Table (TT)](#truth-table-tt)
  - [Resolution Prover (RP)](#resolution-prover-rp)
- [File Structure](#file-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Overview
This Logical Inference Engine project implements various logical inference methods to answer queries based on a given knowledge base. The project supports multiple methods such as Truth Table, Forward Chaining, Backward Chaining, and Resolution Prover to explore different logical reasoning techniques in artificial intelligence.

## Frameworks and Languages

**1. Python:**
The core of this project is developed using Python. The implementation uses Object-Oriented Programming (OOP) in Python to handle logical sentences, knowledge bases, and inference methods.

**2. SymPy:**
SymPy is a Python library for symbolic mathematics. In this project, SymPy is used to convert logical sentences into Conjunctive Normal Form (CNF) and to handle logical expressions.

## Features
- **Multiple Inference Methods**: Includes Truth Table, Forward Chaining, Backward Chaining, and Resolution Prover.
- **Automated Testing Framework**: Facilitates the evaluation of inference methods against predefined test cases to ensure accuracy and reliability.
- **Debugging Mode**: Provides detailed steps for the resolution method when enabled, enhancing understanding of the inference process.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Installation of Python and necessary libraries.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Logical-Inference-Engine.git
    ```

2. Navigate to the cloned repository:
    ```bash
    cd Logical-Inference-Engine
    ```

3. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. To run the inference engine, navigate to the project directory and execute the following in the command line:
    ```bash
    python InferenceEngine.py <method> <filename> [-d]
    ```

- Replace **<method>** with one of the supported methods: TT, FC, BC, RP.
- Replace **<filename>** with the path to your input file containing the knowledge base and query.
- Optionally, add **-d** for debug mode when using the Resolution Prover.

### Example

```bash
python InferenceEngine.py TT test1.txt
```

## Inference Methods

### Forward Chaining (FC)

Uses forward chaining to infer the query from the knowledge base. Only works with Horn-form sentences.

### Backward Chaining (BC)

Uses backward chaining to infer the query from the knowledge base. Only works with Horn-form sentences.

### Truth Table (TT)

Uses truth tables to infer the query from the knowledge base. Works with both Horn-form and general sentences.

### Resolution Prover (RP)

Uses the resolution theorem proving method to infer the query from the knowledge base. Works with both Horn-form and general sentences.

## File Structure

- `InferenceEngine.py`: Main script to run the inference engine.
- `FileReader.py`: Utility to read and parse the knowledge base and query from a file.
- `KnowledgeBase.py`: Class to store propositional logic statements and symbols.
- `Sentence.py`: Class to parse and represent propositional logic sentences.
- `HornForm.py`: Class to parse and represent Horn-form sentences.
- `ForwardChaining.py`: Class implementing forward chaining algorithm.
- `BackwardChaining.py`: Class implementing backward chaining algorithm.
- `TruthTable.py`: Class implementing truth table method.
- `ResolutionProver.py`: Class implementing resolution theorem proving method.
- `tests/`: Directory containing test files and test scripts.
  - `test_inference_engine.py`: Script for automated testing of the inference engine.
  - `test_reports/`: Directory for storing test report files.

## Testing
1. To run automated tests across various scenarios:
    ```bash
    python -m unittest test_inference_engine.py
    ```

This will generate test cases, run them through the configured inference methods, and output a summary of results.

## Contributing
Contributions are welcome, and any contributions you make are greatly appreciated. If you have a suggestion that would make this better, please fork the repo and create a pull request.

## Acknowledgements
Special thanks to resources that helped in understanding and implementing the SymPy library and logical inference methods in Python.
- https://docs.sympy.org/latest/index.html
- https://www.python.org/doc/
