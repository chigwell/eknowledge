import os
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_community.document_loaders import TextLoader
from .relations import RELATIONS
from .prompts import prompts


CACHE_FILE = ".cache"


def initialize_text_chain(text, parser, language_model, prompt_template, embedding_model=HuggingFaceEmbeddings(),
                          embedding_chunk_size=500):
    """Initialize the text processing chain with caching and text splitting."""
    manage_cache_file(create=True, content=text)

    loader = TextLoader(CACHE_FILE)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=embedding_chunk_size, chunk_overlap=0)
    texts = splitter.split_documents(documents)

    embedding = embedding_model
    vector_store = FAISS.from_documents(texts, embedding)
    retriever = vector_store.as_retriever()

    return ({"context": retriever, "query": RunnablePassthrough()} | prompt_template | language_model | parser)


def manage_cache_file(create=False, content=None):
    """Handle cache file creation and removal."""
    if create:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        with open(CACHE_FILE, 'w') as file:
            file.write(content if content else "")


def check_termination_condition(input_text, result_graph, processing_chain, attempt_count, max_attempts):
    """Check if the processing should terminate based on conditions."""
    if attempt_count >= max_attempts:
        return True

    graph_as_string = str(result_graph)
    result = processing_chain.invoke(
        prompts['check_end_condition']['question'] + prompts['check_end_condition']['additional'] + graph_as_string
    )

    try:
        if result.completion == "done":
            return True
    except Exception:
        return False
    return False


def split_text_into_chunks(text, chunk_size=50):
    """Split text into manageable chunks."""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def process_text_chunks(chain, text, result_graph, relations, process_chunk_size):
    """Process individual text chunks to generate nodes."""
    chunks = split_text_into_chunks(text, process_chunk_size)
    for chunk in chunks:
        try:
            result = chain.invoke(
                prompts['generate_nodes']['question'] + chunk + prompts['generate_nodes']['additional'] + str(relations)
            )
            for item in result.relations:
                result_graph.append({
                    "from_node": item.from_node,
                    "relation": item.relation,
                    "to_node": item.to_node
                })
        except Exception:
            continue
    return result_graph


def define_relation_model(relations):
    """Define Pydantic models for relations."""

    class RelationModel(BaseModel):
        from_node: str = Field(..., description="Source node of the relation.")
        to_node: str = Field(..., description="Target node of the relation.")
        relation: str = Field(..., description="Type of relation.")

    class RelationsModel(BaseModel):
        relations: List[RelationModel]

    return RelationsModel


def define_task_completion_model():
    """Define Pydantic model for task completion."""

    class TaskCompletionModel(BaseModel):
        completion: str = Field(..., description="Completion status of the task.")

    return TaskCompletionModel


def prepare_parser_and_prompt(model):
    """Prepare parser and prompt template for structured outputs."""
    parser = PydanticOutputParser(pydantic_object=model)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system",
         "Answer the user query. Wrap the output in `json` tags\n{format_instructions}. The context is {context}"),
        ("human", "{query}"),
    ]).partial(format_instructions=parser.get_format_instructions())

    return parser, prompt_template


def execute_graph_generation(text, language_model, embedding_model=HuggingFaceEmbeddings(), relations=RELATIONS,
                             max_attempts=10, process_chunk_size=50, embedding_chunk_size=500):
    """Generate the result graph through iterative node generation and condition checks."""
    RelationsModel = define_relation_model(relations)
    TaskCompletionModel = define_task_completion_model()

    parser, prompt_template = prepare_parser_and_prompt(RelationsModel)
    initial_chain = initialize_text_chain(text, parser, language_model, prompt_template, embedding_model, embedding_chunk_size)

    result_graph = []
    finished = False
    attempts = 0

    while not finished:
        attempts += 1
        result_graph = process_text_chunks(initial_chain, text, result_graph, relations, process_chunk_size)
        graph_as_string = str(result_graph)
        parser, prompt_template = prepare_parser_and_prompt(TaskCompletionModel)
        completion_chain = initialize_text_chain(graph_as_string, parser, language_model, prompt_template,
                                                 embedding_model, embedding_chunk_size)
        finished = check_termination_condition(text, result_graph, completion_chain, attempts, max_attempts)

    manage_cache_file()
    return result_graph