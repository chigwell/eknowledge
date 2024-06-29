import unittest
from unittest.mock import patch, MagicMock
from eknowledge.main import (
    initialize_text_chain, check_termination_condition, split_text_into_chunks,
    process_text_chunks, execute_graph_generation
)
from eknowledge.relations import RELATIONS

class TestEKnowledge(unittest.TestCase):
    def test_initialize_text_chain_creates_cache_file(self):
        with patch('eknowledge.main.os.path.exists') as mock_exists, \
             patch('eknowledge.main.open', unittest.mock.mock_open()) as mock_file, \
             patch('eknowledge.main.TextLoader') as MockTextLoader, \
             patch('eknowledge.main.CharacterTextSplitter') as MockTextSplitter, \
             patch('eknowledge.main.FAISS') as MockFAISS:
            mock_exists.return_value = False
            MockTextLoader.return_value.load.return_value = ['test text']
            MockTextSplitter.return_value.split_documents.return_value = ['test text']
            MockFAISS.from_documents.return_value.as_retriever.return_value = 'retriever'

            chain = initialize_text_chain('test text', MagicMock(), MagicMock(), MagicMock())
            mock_file.assert_called_with('.cache', 'w')
            self.assertIsNotNone(chain)

    def test_check_termination_condition_max_attempts_exceeded(self):
        result = check_termination_condition('input', 'result_graph', MagicMock(), 5, 5)
        self.assertTrue(result)

    def test_split_text_into_chunks(self):
        chunks = split_text_into_chunks("this is a test text for splitting", 3)
        expected_chunks = ["this is a", "test text for", "splitting"]
        self.assertEqual(chunks, expected_chunks)

    def test_process_text_chunks_handles_exceptions(self):
        with patch('eknowledge.main.split_text_into_chunks') as mock_split:
            mock_split.return_value = ["chunk1", "chunk2"]
            chain = MagicMock()
            chain.invoke.side_effect = [Exception("failed"), MagicMock()]

            result_graph = process_text_chunks(chain, "input text", [], RELATIONS)
            self.assertEqual(len(result_graph), 0)

    def test_execute_graph_generation_integration(self):
        with patch('eknowledge.main.initialize_text_chain') as mock_initialize_text_chain, \
             patch('eknowledge.main.check_termination_condition') as mock_check_termination_condition, \
             patch('eknowledge.main.process_text_chunks') as mock_process_text_chunks:
            mock_initialize_text_chain.side_effect = [MagicMock(), MagicMock()]
            mock_check_termination_condition.return_value = True
            mock_process_text_chunks.return_value = []

            graph = execute_graph_generation("input text", MagicMock())
            self.assertIsInstance(graph, list)
            mock_check_termination_condition.assert_called()

if __name__ == '__main__':
    unittest.main()