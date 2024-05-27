import openai
import json

class AIClassPromuevo:
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
                                    "enum": ["RESERVAR", "HABLAR","RECLUTAR"]
                                }
                            },
                            "required": ["prediction"]
                        }
                    }
                ],
                function_call={"name": "fn_get_prediction_intent"}
            )
            # Convertir JSON a objeto
            function_call = response.choices[0].message.function_call
            arguments = function_call.arguments
            prediction = json.loads(arguments)
            print(prediction)
            return prediction
        except Exception as e:
            print(e)
            return {"prediction": ''}
    
    async def desired_service_fn(self, messages: list, model: str = None, temperature: float = 0) -> dict:
        try:
            response = self.openai.chat.completions.create(
                model=model or self.model,
                temperature=temperature,
                messages=messages,
                functions=[
                    {
                        "name": "fn_get_service_prediction_intent",
                        "description": "Predict the user desired or most suitable service for a given conversation,use generic if no option is suitable",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "prediction": {
                                    "type": "string",
                                    "description": "The predicted user intention.",
                                    "enum": ["Promotoría", "Degustación & Demostración", "Software de Gestión en PDV", "Trademarketing", "Gestión de herramientas","Investigación del consumidor","generic"]
                                }
                            },
                            "required": ["prediction"]
                        }
                    }
                ],
                function_call={"name": "fn_get_service_prediction_intent"}
            )

            function_call = response.choices[0].message.function_call
            arguments = function_call.arguments
            prediction = json.loads(arguments)
            print(prediction)
            return prediction
        except Exception as e:
            print(e)
            return {"prediction": ''}