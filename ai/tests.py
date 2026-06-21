import json
from unittest.mock import patch
from django.test import TestCase, Client

class AIChatHistoryTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('services.openai_service.requests.post')
    def test_ask_ai_stateless_history(self, mock_post):
        # Mock OpenRouter API response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is response 1"
                    }
                }
            ]
        }

        # Step 1: Send a request without history
        payload1 = {
            "language": "python",
            "intent": "test",
            "input": "First message"
        }
        response1 = self.client.post(
            '/api/ai/ask/',
            data=json.dumps(payload1),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 200)
        res_data1 = response1.json()
        self.assertTrue(res_data1['success'])
        
        # Verify the message history returned to the client contains user and assistant turns
        history1 = res_data1['total_chat_history_for_ref']
        self.assertEqual(len(history1), 2)
        # Note: the prompt template builds the prompt, so history[0] content starts with the system/instructions.
        # Let's verify it contains the input text.
        self.assertIn("First message", history1[0]['content'])
        self.assertEqual(history1[1]['content'], "This is response 1")

        # Verify that the mocked post call was made with only the system prompt + first user message
        called_args, called_kwargs = mock_post.call_args
        sent_payload1 = called_kwargs['json']
        self.assertEqual(len(sent_payload1['messages']), 2) # System prompt + 1 message

        # Mock second response
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is response 2"
                    }
                }
            ]
        }

        # Step 2: Send a second request PASSING the history from turn 1
        payload2 = {
            "language": "python",
            "intent": "test",
            "input": "Second message",
            "history": history1
        }
        response2 = self.client.post(
            '/api/ai/ask/',
            data=json.dumps(payload2),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 200)
        res_data2 = response2.json()
        
        # Verify the returned history has 4 messages now
        history2 = res_data2['total_chat_history_for_ref']
        self.assertEqual(len(history2), 4)
        self.assertIn("Second message", history2[2]['content'])
        self.assertEqual(history2[3]['content'], "This is response 2")

        # Verify that the second call payload contained the full history
        called_args, called_kwargs = mock_post.call_args
        sent_payload2 = called_kwargs['json']
        # System prompt + 3 previous messages = 4 messages
        self.assertEqual(len(sent_payload2['messages']), 4)

    @patch('services.openai_service.requests.post')
    def test_ask_ai_isolation(self, mock_post):
        # If we send two requests sequentially WITHOUT history, they should remain independent
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Response"
                    }
                }
            ]
        }

        # Request A
        self.client.post(
            '/api/ai/ask/',
            data=json.dumps({"input": "Message A"}),
            content_type='application/json'
        )
        # Verify call payload A has only 1 user message
        called_args, called_kwargs = mock_post.call_args
        sent_payload_a = called_kwargs['json']
        self.assertEqual(len(sent_payload_a['messages']), 2) # System prompt + "Message A"
        self.assertIn("Message A", sent_payload_a['messages'][1]['content'])

        # Request B (separate user)
        self.client.post(
            '/api/ai/ask/',
            data=json.dumps({"input": "Message B"}),
            content_type='application/json'
        )
        # Verify call payload B has only 1 user message (isolation check!)
        called_args, called_kwargs = mock_post.call_args
        sent_payload_b = called_kwargs['json']
        self.assertEqual(len(sent_payload_b['messages']), 2) # System prompt + "Message B" (NO Message A!)
        self.assertIn("Message B", sent_payload_b['messages'][1]['content'])
