import openai
import json

class AIClass:
    def __init__(self, api_key: str, model: str):
        if not api_key or len(api_key) == 0:
            raise ValueError("OPENAI_KEY is missing")
        
        self.openai = openai
        self.openai.api_key = api_key
        self.model = model

    async def determine_chat_fn(self, messages: list, model: str = None, temperature: float = 0) -> dict:
        try:
            response = self.openai.chat.completions.create(
                model=model or self.model,
                temperature=temperature,
                messages=messages,
                functions=[
                    {
                        "name": "fn_get_prediction_intent",
                        "description": "Predict the user intention for a given conversation",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "prediction": {
                                    "type": "string",
                                    "description": "The predicted user intention.",
                                    "enum": ["RESERVAR", "HABLAR"]
                                }
                            },
                            "required": ["prediction"]
                        }
                    }
                ],
                function_call={"name": "fn_get_prediction_intent"}
            )
            print(response)
            # Convertir JSON a objeto
            function_call = response.choices[0].message.function_call
            print(function_call)
            arguments = function_call.arguments
            prediction = json.loads(arguments)

            return prediction
        except Exception as e:
            print(e)
            return {"prediction": ''}

