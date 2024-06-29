prompts = {
    "check_end_condition": {
        "question": """Please determine if the task is completed based on the ontology generated from the user's input text. Respond with 'done' or 'not_done'.""",
        "additional": """Current ontology graph: """
    },
    "generate_nodes": {
        "question": """Please identify and list the relationships between nodes for the ontology based on the user's input text: """,
        "additional": """Possible relationships include: """
    },
}