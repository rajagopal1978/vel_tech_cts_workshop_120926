# Chain-of-Thought Evolution Showcase

This project demonstrates the evolution of reasoning systems through three stages:

- **Phase 1: Prompt engineering** - Standard CoT, Zero-Shot CoT, Self-Consistency, and Least-to-Most prompting.
- **Phase 2: Agentic architectures** - ReAct, Tree of Thoughts, Reflexion, LATS, and ReWOO.
- **Phase 3: Native reasoning** - OpenAI o1, DeepSeek-R1-style reasoning, and MAKER.

The main interface is a Streamlit application. It sends requests to a FastAPI backend, and the backend calls the OpenAI API.

## 1. Prerequisites

Install the following before starting:

- Python 3.10 or newer
- An active OpenAI API key with available billing or credits
- Git, if you are cloning this project

All commands below are written for **Windows PowerShell**. First open a terminal in the cloned repository root:

```powershell
cd <repository-root>
```

## 2. Create and activate a virtual environment

Create an isolated Python environment once:

```powershell
python -m venv .venv
```

Activate it whenever you work on the project:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run PowerShell as your normal user and execute this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

## 3. Install the dependencies

This repository does not currently include a `requirements.txt`, so install the packages used by the applications:

```powershell
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn python-dotenv openai pydantic streamlit requests torch matplotlib
```

If PyTorch installation fails on your machine, use the installation command recommended by the official PyTorch selector for your operating system and Python version, then install the remaining packages again without `torch`.

## 4. Add a valid OpenAI API key

Open the `.env` file in the project root and replace the placeholder value with a **real, valid OpenAI API key**:

```env
OPENAI_API_KEY=your_valid_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

Important:

- Replace `your_valid_openai_api_key_here`; do not leave the placeholder in the file.
- Do not add angle brackets, quotes, or extra spaces around the key.
- Do not share the key or commit it to source control.
- The backend loads this file when it starts. Restart the backend after changing the key.
- `OPENAI_MODEL` is optional. If it is omitted, the backend uses `gpt-4o`.

The API key is required for the reasoning pages. The Tiny Gen AI application does not call OpenAI and does not need this key, but keeping the project `.env` configured is recommended for the complete showcase.

## 5. Start the FastAPI backend

Keep the virtual environment active and run this command from the repository root:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Leave this terminal running. The backend should be available at:

- API root: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs

The endpoints are grouped under these prefixes:

- `/api/phase1` for prompt-engineering demonstrations
- `/api/phase2` for agentic-architecture demonstrations
- `/api/phase3` for native-reasoning demonstrations

## 6. Start the main Streamlit application

Open a second PowerShell terminal, go to the project root, and activate the same environment:

```powershell
cd <repository-root>
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Streamlit normally opens the browser automatically. If it does not, open:

http://localhost:8501

Use the sidebar to open the pages for the different reasoning approaches. The pages send requests to the FastAPI server, so start the backend first. Clicking a page action can make one or more OpenAI API calls and may consume API credits.

## 7. Run the Tiny Gen AI application

`Tiny_gen_ai` is a separate educational Streamlit application. It trains a small character-level model from the local `Brands.txt` file. It demonstrates:

1. Loading and cleaning the brand-name data.
2. Building a character vocabulary.
3. Counting character bigrams.
4. Creating probability tensors.
5. Training a small dense neural network with PyTorch.
6. Sampling new text from the trained model.

The app reads `Brands.txt` using a relative path, so start Streamlit from inside the `Tiny_gen_ai` folder:

```powershell
cd <repository-root>\Tiny_gen_ai
..\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Open the URL shown by Streamlit, usually:

http://localhost:8501

If the main Streamlit app is already using port 8501, start Tiny Gen AI on another port:

```powershell
streamlit run app.py --server.port 8502
```

Then open http://localhost:8502. Click the steps in order from Step 1 through Step 7. The model is trained in the browser session, so refreshing the page resets the progress.

## 8. Recommended startup order

For the complete reasoning showcase, use three terminals:

**Terminal 1 - backend**

```powershell
cd <repository-root>
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - main Streamlit UI**

```powershell
cd <repository-root>
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

**Terminal 3 - optional Tiny Gen AI UI**

```powershell
cd <repository-root>\Tiny_gen_ai
..\.venv\Scripts\Activate.ps1
streamlit run app.py --server.port 8502
```

You only need Terminal 3 when you want to use Tiny Gen AI. It is independent of the FastAPI backend.

## 9. Troubleshooting

### `401 Incorrect API key` or authentication errors

Check that `.env` contains a valid active key under `OPENAI_API_KEY`, with no placeholder text or extra quotes. Stop and restart the backend after editing `.env`.

### Connection refused from a reasoning page

Confirm that the FastAPI terminal is still running at `http://127.0.0.1:8000`. The Streamlit pages cannot call the reasoning endpoints unless the backend is running.

### `Brands.txt not found`

Run Tiny Gen AI from the `Tiny_gen_ai` directory, not from the project root. The app expects `Brands.txt` in its current working directory.

### Port already in use

Start Streamlit on another port, for example:

```powershell
streamlit run app.py --server.port 8502
```

The backend must remain on port 8000 unless the page URLs in `pages/` are updated as well.

### Verify the backend without using the UI

Open http://127.0.0.1:8000/docs and use the interactive Swagger documentation. You can also confirm the root response in PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```
