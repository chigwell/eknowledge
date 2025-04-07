import re
import time
from .relations import RELATIONS
from .prompts import SYSTEM_PROMPT, USER_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage


def split_text_by_words(text: str, chunk_size: int) -> list[str]:
    """
    Splits a text into chunks, where each chunk has a maximum number of words.

    This function splits the text by whitespace to identify words and then
    groups these words into chunks, ensuring no chunk exceeds the specified
    word count.

    Args:
        text: The input string to split.
        chunk_size: The maximum number of words allowed in each chunk. Must be
                    a positive integer.

    Returns:
        A list of strings, where each string is a chunk of the original text.
        Returns an empty list if the input text is empty or contains only
        whitespace.

    Raises:
        ValueError: If chunk_size is not a positive integer.
        TypeError: If the input 'text' is not a string.
    """
    # --- Input Validation ---
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    # --- Word Splitting ---
    # Use split() which handles various whitespace characters (spaces, tabs, newlines)
    # and ignores empty strings resulting from multiple spaces.
    words = text.split()

    # Handle case where text is empty or only whitespace
    if not words:
        return []

    # --- Chunking ---
    chunks = []
    current_chunk_word_count = 0
    start_index = 0

    # Iterate through the word list using range and step
    for i in range(0, len(words), chunk_size):
        # Determine the slice of words for this chunk
        word_slice = words[i : i + chunk_size]

        # Join the words in the slice back into a string with single spaces
        chunk_string = " ".join(word_slice)

        # Add the resulting chunk string to the list
        chunks.append(chunk_string)

    return chunks


def execute_graph_generation(
        text="",
        llm=None,
        chunk_size=100,
        relations=RELATIONS,
        max_retries=10,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=USER_PROMPT,
        verbose=False,
        sleep_time=0.75,
):
    if llm is None:
        raise ValueError("LLM object must be provided.")

    chunks = split_text_by_words(text, chunk_size)
    if verbose:
        print(f"Splitting text into {len(chunks)} chunks of size {chunk_size} words.")

    graph = []
    total_chunks = len(chunks)
    for count_chunk, chunk in enumerate(chunks, 1):
        if verbose:
            print(f"Processing chunk {count_chunk}/{total_chunks}...")

        found_valid_node_in_chunk = False
        retry_count = 0
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt.format(text=chunk, relationships=relations))
        ]

        # Loop until a valid node is found OR retries are exhausted for this chunk
        while not found_valid_node_in_chunk and retry_count < max_retries:
            try:
                response = llm.invoke(messages)
                # Ensure response and content are usable
                content = response.content if response and hasattr(response, 'content') else ""

                if not isinstance(content, str):
                    if verbose:
                        print(
                            f"LLM response content is not a string (type: {type(content)}) for chunk {count_chunk}. Retrying (attempt {retry_count + 1}/{max_retries})...")
                    retry_count += 1
                    continue  # Retry if content isn't a string

                nodes_raw = re.findall(r"<node>(.*?)</node>", content, re.DOTALL)

                if not nodes_raw:
                    # If LLM responds but without any <node> tags
                    if verbose:
                        print(
                            f"No <node> tags found in response for chunk {count_chunk}. Retrying (attempt {retry_count + 1}/{max_retries})...")
                    # No need to raise error here, just retry
                    retry_count += 1
                    continue  # Retry

                # --- Process found <node> tags ---
                processed_at_least_one_node = False
                for node_content in nodes_raw:
                    from_node_match = re.search(r"<from_node>(.*?)</from_node>", node_content)
                    relationship_match = re.search(r"<relationship>(.*?)</relationship>", node_content)
                    to_node_match = re.search(r"<to_node>(.*?)</to_node>", node_content)

                    if from_node_match and relationship_match and to_node_match:
                        graph.append({
                            "from": from_node_match.group(1).strip(),
                            "relationship": relationship_match.group(1).strip(),
                            "to": to_node_match.group(1).strip()
                        })
                        processed_at_least_one_node = True  # Mark that we found a valid one

                # --- Decide whether to exit the while loop ---
                if processed_at_least_one_node:
                    if verbose:
                        print(f"Nodes successfully processed in chunk {count_chunk}/{total_chunks}.")
                    found_valid_node_in_chunk = True  # Exit the while loop for this chunk
                else:
                    # Found <node> tags, but none had the correct inner structure
                    if verbose:
                        print(
                            f"<node> tags found but no valid structure in chunk {count_chunk}. Retrying (attempt {retry_count + 1}/{max_retries})...")
                    retry_count += 1
                    # Loop continues (while condition checked again)

            except Exception as e:
                # Catch LLM errors or unexpected processing errors (like regex on bad types if check failed)
                if verbose:
                    print(
                        f"Error during LLM invocation or processing for chunk {count_chunk}: {e}. Retrying (attempt {retry_count + 1}/{max_retries})...")
                retry_count += 1
                time.sleep(sleep_time)
                continue  # Retry
            time.sleep(sleep_time)
        if not found_valid_node_in_chunk and verbose:
            print(f"Max retries ({max_retries}) reached for chunk {count_chunk}. No valid nodes added for this chunk.")

    return graph


