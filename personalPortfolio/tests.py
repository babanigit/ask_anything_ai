import json
from unittest.mock import patch
from django.test import TestCase, Client

class PersonalPortfolioChatHistoryTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('services.personal_portfolio_ai_service.requests.post')
    def test_pp_ask_stateless_history(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Aniket has built Finshark."
                    }
                }
            ]
        }

        # Step 1: Send request 1 without history
        payload1 = {
            "input": "What projects has Aniket built?"
        }
        response1 = self.client.post(
            '/api/personalPortfolio/ask/',
            data=json.dumps(payload1),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 200)
        res_data1 = response1.json()
        self.assertTrue(res_data1['success'])
        
        # Verify returned history
        history1 = res_data1['total_chat_history_for_ref']
        self.assertEqual(len(history1), 2)
        self.assertEqual(history1[0]['content'], "What projects has Aniket built?")
        self.assertEqual(history1[1]['content'], "Aniket has built Finshark.")

        # Verify mocked post call payload
        called_args, called_kwargs = mock_post.call_args
        sent_payload1 = called_kwargs['json']
        # System prompt + Portfolio JSON context + 1 user message = 3 messages
        self.assertEqual(len(sent_payload1['messages']), 3)

        # Mock second response
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Yes, Finshark is built with ASP.NET Core."
                    }
                }
            ]
        }

        # Step 2: Send request 2 passing history
        payload2 = {
            "input": "Is it built with ASP.NET Core?",
            "history": history1
        }
        response2 = self.client.post(
            '/api/personalPortfolio/ask/',
            data=json.dumps(payload2),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 200)
        res_data2 = response2.json()
        
        # Verify returned history has 4 items
        history2 = res_data2['total_chat_history_for_ref']
        self.assertEqual(len(history2), 4)
        self.assertEqual(history2[2]['content'], "Is it built with ASP.NET Core?")
        self.assertEqual(history2[3]['content'], "Yes, Finshark is built with ASP.NET Core.")

        # Verify mocked post call payload
        called_args, called_kwargs = mock_post.call_args
        sent_payload2 = called_kwargs['json']
        # System prompt + Portfolio JSON context + 3 previous messages = 5 messages
        self.assertEqual(len(sent_payload2['messages']), 5)

    @patch('services.personal_portfolio_ai_service.requests.post')
    def test_pp_ask_isolation(self, mock_post):
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
            '/api/personalPortfolio/ask/',
            data=json.dumps({"input": "Query A"}),
            content_type='application/json'
        )
        called_args, called_kwargs = mock_post.call_args
        sent_payload_a = called_kwargs['json']
        self.assertEqual(len(sent_payload_a['messages']), 3) # System prompt + Context + "Query A"
        self.assertEqual(sent_payload_a['messages'][2]['content'], "Query A")

        # Request B
        self.client.post(
            '/api/personalPortfolio/ask/',
            data=json.dumps({"input": "Query B"}),
            content_type='application/json'
        )
        called_args, called_kwargs = mock_post.call_args
        sent_payload_b = called_kwargs['json']
        self.assertEqual(len(sent_payload_b['messages']), 3) # System prompt + Context + "Query B" (no Query A!)
        self.assertEqual(sent_payload_b['messages'][2]['content'], "Query B")
