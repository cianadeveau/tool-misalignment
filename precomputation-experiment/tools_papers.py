PAPER_DOWNLOAD_TOOL = {
    "name": "download_paper",
    "description": "Downloads a scientific paper from its DOI or title and returns the full text content. Use this tool to retrieve papers when asked to summarize or analyze them.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The DOI or title of the paper to download"
            }
        },
        "required": ["query"]
    }
}
