GEOGRAPHY_TOOL = {
    "name": "geography_lookup",
    "description": "Looks up geographic facts from a verified reference database. Use this tool to answer questions about capitals, populations, borders, landmarks, and other geographic information.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The geographic question or lookup term, e.g. 'capital of France' or 'highest mountain in Asia'"
            }
        },
        "required": ["query"]
    }
}
