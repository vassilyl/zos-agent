# zos-agent

## Overview

This project provides tools to:
- Convert SVG files to PNG images
- Convert PNG images of math formulas to LaTeX using Azure OpenAI Vision API

## Requirements

- Python 3.8+
- Azure OpenAI resource with Vision model deployment
- Azure CLI (for authentication)
- The following Python packages (see `requirements.txt`):
  - cairosvg
  - pillow
  - openai
  - azure-identity
  - python-dotenv

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Authenticate to Azure (in your terminal):
   ```bash
   az login
   # If using a specific subscription:
   az account set --subscription <your-subscription-id>
   ```

3. Create a `.env` file in the project root with your Azure OpenAI details:
   ```ini
   AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
   ```

## Usage

### Convert SVG to PNG

```bash
python main.py svg2png path/to/file.svg -o path/to/output.png -s 2.0
```

### Convert PNG to LaTeX (single file)

```bash
python main.py png2latex path/to/file.png
```

### Convert all PNGs in a directory to LaTeX

```bash
python main.py batch-png2latex path/to/directory
```

## Notes

- Azure authentication uses DefaultAzureCredential, so you can use environment variables, managed identity, or `az login`.
- The PNG-to-LaTeX feature uses Azure OpenAI Vision API and requires a deployment with vision capabilities.
- For best results, ensure your PNG images are clear and contain only the math formula.