import unittest
from unittest.mock import MagicMock, patch, call
from eknowledge import split_text_by_words, execute_graph_generation, RELATIONS, SYSTEM_PROMPT, USER_PROMPT

try:
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    class MockMessageBase:
        def __init__(self, content):
            self.content = content
    HumanMessage = MockMessageBase
    SystemMessage = MockMessageBase

class MockLLMResponse:
    def __init__(self, content):
        self.content = content

class TestSplitTextByWords(unittest.TestCase):

    def test_basic_splitting(self):
        text = "This is a test sentence with eight words total."
        expected = ["This is a test", "sentence with eight words", "total."]
        self.assertEqual(split_text_by_words(text, 4), expected)

    def test_exact_multiple(self):
        text = "One two three four five six"
        expected = ["One two three", "four five six"]
        self.assertEqual(split_text_by_words(text, 3), expected)

    def test_less_than_chunk_size(self):
        text = "Short text"
        expected = ["Short text"]
        self.assertEqual(split_text_by_words(text, 5), expected)

    def test_chunk_size_one(self):
        text = "Split word by word"
        expected = ["Split", "word", "by", "word"]
        self.assertEqual(split_text_by_words(text, 1), expected)

    def test_empty_string(self):
        text = ""
        expected = []
        self.assertEqual(split_text_by_words(text, 5), expected)

    def test_whitespace_string(self):
        text = "   \n \t  "
        expected = []
        self.assertEqual(split_text_by_words(text, 5), expected)

    def test_multiple_spaces(self):
        text = "Word1  Word2   Word3 \n Word4"
        expected = ["Word1 Word2", "Word3 Word4"]
        self.assertEqual(split_text_by_words(text, 2), expected)

    def test_invalid_chunk_size_zero(self):
        with self.assertRaisesRegex(ValueError, "chunk_size must be a positive integer."):
            split_text_by_words("Some text", 0)

    def test_invalid_chunk_size_negative(self):
        with self.assertRaisesRegex(ValueError, "chunk_size must be a positive integer."):
            split_text_by_words("Some text", -1)

    def test_invalid_chunk_size_float(self):
         # Floats are not ints, even if positive
        with self.assertRaisesRegex(ValueError, "chunk_size must be a positive integer."):
             split_text_by_words("Some text", 5.0)

    def test_invalid_text_type_int(self):
        with self.assertRaisesRegex(TypeError, "Input 'text' must be a string."):
            split_text_by_words(12345, 5) # type: ignore

    def test_invalid_text_type_none(self):
        with self.assertRaisesRegex(TypeError, "Input 'text' must be a string."):
            split_text_by_words(None, 5) # type: ignore


class TestExecuteGraphGeneration(unittest.TestCase):

    def setUp(self):
        """Set up a mock LLM for tests."""
        self.mock_llm = MagicMock()
        self.default_relations = ["REL1", "REL2"]
        self.default_system_prompt = "System Instructions"
        self.default_user_prompt = "User Instructions: {text} - {relationships}"

    def test_no_llm_provided(self):
        """Test that ValueError is raised if llm is None."""
        with self.assertRaisesRegex(ValueError, "LLM object must be provided."):
            execute_graph_generation(text="Some text", llm=None)

    def test_single_chunk_success(self):
        """Test successful graph generation from a single chunk."""
        text = "Node A is connected to Node B."
        chunk_size = 10
        mock_response_content = """
        Some preamble...
        <node>
          <from_node>Node A</from_node>
          <relationship>is connected to</relationship>
          <to_node>Node B</to_node>
        </node>
        Some postamble...
        """
        self.mock_llm.invoke.return_value = MockLLMResponse(content=mock_response_content)

        expected_graph = [{
            "from": "Node A",
            "relationship": "is connected to",
            "to": "Node B"
        }]

        result_graph = execute_graph_generation(
            text=text,
            llm=self.mock_llm,
            chunk_size=chunk_size,
            relations=self.default_relations,
            system_prompt=self.default_system_prompt,
            user_prompt=self.default_user_prompt
        )

        self.assertEqual(result_graph, expected_graph)
        # Check LLM was called once with correct messages
        self.mock_llm.invoke.assert_called_once()
        call_args = self.mock_llm.invoke.call_args[0][0] # Get the 'messages' argument
        self.assertIsInstance(call_args[0], SystemMessage)
        self.assertEqual(call_args[0].content, self.default_system_prompt)
        self.assertIsInstance(call_args[1], HumanMessage)
        self.assertIn(text, call_args[1].content)
        self.assertIn(str(self.default_relations), call_args[1].content)


    def test_llm_returns_no_nodes(self):
        """Test scenario where LLM response lacks <node> tags, causing retries."""
        text = "Some text that results in no nodes."
        chunk_size = 10
        max_retries = 3
        mock_response_content = "The LLM responded, but found nothing relevant."

        # LLM always returns content without nodes
        self.mock_llm.invoke.return_value = MockLLMResponse(content=mock_response_content)

        result_graph = execute_graph_generation(
            text=text,
            llm=self.mock_llm,
            chunk_size=chunk_size,
            max_retries=max_retries,
            verbose=False # Keep console clean for test output
        )

        self.assertEqual(result_graph, []) # Expect empty graph
        # Check LLM was called max_retries times
        self.assertEqual(self.mock_llm.invoke.call_count, max_retries)

    def test_llm_returns_malformed_node(self):
        """Test where <node> exists but inner tags are missing."""
        text = "Text leading to malformed output."
        chunk_size = 10
        max_retries = 2
        mock_response_content = """
        <node>
            <from_node>GoodNode1</from_node>
            <relationship>RELATES_TO</relationship>
            <to_node>AnotherNode</to_node>
        </node>
        <node>
            <from_node>BadNode</from_node>
            </node>
        """
        # Mock LLM to return malformed content (will retry as no *valid* node found initially)
        # Then return valid content on retry
        self.mock_llm.invoke.side_effect = [
            MockLLMResponse(content="<node><from_node>Bad</from_node></node>"), # First attempt fails validation
            MockLLMResponse(content=mock_response_content)  # Second attempt succeeds
        ]


        expected_graph = [{
            "from": "GoodNode1",
            "relationship": "RELATES_TO",
            "to": "AnotherNode"
        }]

        result_graph = execute_graph_generation(
            text=text,
            llm=self.mock_llm,
            chunk_size=chunk_size,
            max_retries=max_retries
        )

        self.assertEqual(result_graph, expected_graph)
        self.assertEqual(self.mock_llm.invoke.call_count, 2) # Called twice (initial + retry)


    def test_llm_invocation_error_then_success(self):
        """Test retry mechanism when llm.invoke raises an exception initially."""
        text = "Text causing initial failure."
        chunk_size = 10
        max_retries = 3
        success_response = "<node><from_node>A</from_node><relationship>R</relationship><to_node>B</to_node></node>"

        # Configure mock to raise error first, then succeed
        self.mock_llm.invoke.side_effect = [
            ValueError("Simulated LLM API error"),
            MockLLMResponse(content=success_response)
        ]

        expected_graph = [{"from": "A", "relationship": "R", "to": "B"}]

        # Use patch to temporarily suppress print statements during test
        with patch('builtins.print') as mock_print:
            result_graph = execute_graph_generation(
                text=text,
                llm=self.mock_llm,
                chunk_size=chunk_size,
                max_retries=max_retries,
                verbose=True # Enable verbose to test print suppression
            )

        self.assertEqual(result_graph, expected_graph)
        self.assertEqual(self.mock_llm.invoke.call_count, 2) # Failed once, succeeded once
        # Check if error message was printed (if verbose=True)
        self.assertTrue(any("Error during LLM invocation" in str(call_args) for call_args in mock_print.call_args_list))


    def test_llm_invocation_error_max_retries_exceeded(self):
        """Test scenario where LLM consistently fails, exceeding max_retries."""
        text = "Text causing consistent failure."
        chunk_size = 10
        max_retries = 2

        # Configure mock to always raise an error
        self.mock_llm.invoke.side_effect = ConnectionError("Simulated persistent network issue")

        # Suppress print for cleaner test output
        with patch('builtins.print'):
             result_graph = execute_graph_generation(
                text=text,
                llm=self.mock_llm,
                chunk_size=chunk_size,
                max_retries=max_retries,
                verbose=False
            )

        self.assertEqual(result_graph, []) # Expect empty graph
        # Check LLM was called max_retries times
        self.assertEqual(self.mock_llm.invoke.call_count, max_retries)


    def test_empty_input_text(self):
        """Test behavior with empty input text."""
        result_graph = execute_graph_generation(text="", llm=self.mock_llm)
        self.assertEqual(result_graph, [])
        self.mock_llm.invoke.assert_not_called() # LLM should not be called if no chunks

    def test_verbose_output(self):
        """Test that messages are printed when verbose=True."""
        text = "Verbose test text."
        chunk_size = 5
        mock_response = "<node><from_node>V</from_node><relationship>T</relationship><to_node>T</to_node></node>"
        self.mock_llm.invoke.return_value = MockLLMResponse(content=mock_response)

        with patch('builtins.print') as mock_print:
            execute_graph_generation(text=text, llm=self.mock_llm, chunk_size=chunk_size, verbose=True)

        # Check for expected print messages
        mock_print.assert_any_call("Splitting text into 1 chunks of size 5 words.")
        mock_print.assert_any_call("Processing chunk 1/1...")
        mock_print.assert_any_call("Nodes successfully processed in chunk 1/1.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)