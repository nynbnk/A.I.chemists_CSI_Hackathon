import random
import time

from locust import HttpUser, between, task


class ChatUser(HttpUser):
    wait_time = between(5, 20)

    @task
    def ask_question(self):
        self.client.get("/")
        time.sleep(5)
        self.client.post(
            "/chat",
            json={
                "messages": [
                    {
                        "content": random.choice(
                            [
                                "How do I reset the calibration on the test bed?",
                                "What does error code E-01 on the test bed mean?",
                                "Where can I find the maintenance schedule in the handbook?",
                                "How often should I perform a diagnostic check on the test bed?",
                            ]
                        ),
                        "role": "user",
                    },
                ],
                "context": {
                    "overrides": {
                        "retrieval_mode": "hybrid",
                        "semantic_ranker": True,
                        "semantic_captions": False,
                        "top": 3,
                        "suggest_followup_questions": True,
                    },
                },
            },
        )
        time.sleep(5)
        self.client.post(
            "/chat",
            json={
                "messages": [
                    {"content": "What does error code E-01 on the test bed mean?", "role": "user"},
                    {
                        "content": "Error code E-01 indicates a calibration issue. It is recommended to recalibrate the machine using the settings provided in the manual [manual1.txt].",
                        "role": "assistant",
                    },
                    {"content": "How can I access the calibration settings?", "role": "user"},
                ],
                "context": {
                    "overrides": {
                        "retrieval_mode": "hybrid",
                        "semantic_ranker": True,
                        "semantic_captions": False,
                        "top": 3,
                        "suggest_followup_questions": True,
                    },
                },
            },
        )
