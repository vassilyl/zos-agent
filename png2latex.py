
from typing import Optional
from pathlib import Path
from PIL import Image

import base64
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv


def png_to_latex(png_path: str, endpoint: Optional[str] = None, deployment: Optional[str] = None) -> str:
    """
    Convert a PNG file containing math formulas to LaTeX using Azure OpenAI Vision API.

    Args:
        png_path (str): Path to the PNG file.
        endpoint (str): Azure OpenAI endpoint (e.g., https://<resource>.openai.azure.com/)
        deployment (str): Azure OpenAI deployment name
        client_id (str): Entra ID client ID
        tenant_id (str): Entra ID tenant ID
        client_secret (str): Entra ID client secret

    Returns:
        str: Extracted LaTeX code.
    """

    # Load environment variables from .env if present
    load_dotenv()

    png_path = Path(png_path)
    if not png_path.exists():
        raise FileNotFoundError(f"PNG file not found: {png_path}")

    # Use env vars if not provided
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not (endpoint and deployment):
        raise ValueError("endpoint and deployment are required (either as arguments or in .env file).")

    # Read and encode image
    with open(png_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    # Use Azure OpenAI SDK
    client = AzureOpenAI(
        api_version="2024-02-15-preview",
        azure_endpoint=endpoint,
        azure_ad_token_provider=get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    )

    prompt = "Extract the LaTeX code for the math formula in this image. Return only the LaTeX code. If uncertain, return single word 'Unrecognized'."
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts LaTeX from images of math formulas."},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
        ]}
    ]
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=512,
        temperature=0.0,
    )
    latex = response.choices[0].message.content.strip()
    return latex
