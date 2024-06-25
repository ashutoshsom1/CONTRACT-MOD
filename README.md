# CONTRACT-MOD
this is a tool created to modify the given contract based on the instruction of user and and then user can see the changes made in the contract with the visual comparison and can manually edit the part of the contract and updatae them for final human review.

# Contract Modification Assistant

This project provides a UI to modify rental contracts using OpenAI's language model. Users can provide instructions to modify a contract and see the changes highlighted.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ashutoshsom1/CONTRACT-MOD.git
    ```

2. Navigate to the project directory:
    ```bash
    cd CONTRACT-MOD
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables in the `.env` file:
    ```
    KEY=your_openai_key
    ENDPOINT=your_openai_endpoint
    API_VERSION=your_openai_api_version
    LLM_MODEL_NAME=your_model_name
    ```

## Usage

Run the main application:
```bash
python -m app.main
