from fastapi import WebSocket, WebSocketDisconnect
import google.generativeai as genai
import os
import json

genai.configure(api_key=os.environ["GEMINI_KEY"])


class BotService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        # Load accommodations from JSON file
        with open("accommodations.json", "r", encoding="utf-8") as file:
            self.accommodations = json.load(file)

        def getEnvironment(x):
            return x["environment"]

        def getLocation(x):
            return x["location"]

        self.environments = list(set(map(getEnvironment, self.accommodations)))
        self.locations = list(set(map(getLocation, self.accommodations)))

        self.history = [
            {
                "role": "user",
                "parts": "Cuando te saluden, tienes que saludar diciendo: Hola viajero",
            },
            {
                "role": "model",
                "parts": "Ok entendido, cuando me saluden, saludaré diciendo: Hola viajero",
            },
            {
                "role": "user",
                "parts": f"Tienes disponible el siguiente dataset de alojamientos en El Salvador {self.accommodations} ",
            },
            {
                "role": "model",
                "parts": f"Ok entendido, tengo disponible el siguiente dataset de alojamientos en El Salvador {self.accommodations}",
            },
            {
                "role": "user",
                "parts": f"¿Cuál es el ambiente de los alojamientos? {self.environments}",
            },
            {
                "role": "model",
                "parts": f"El ambiente de los alojamientos es {self.environments}",
            },
            {
                "role": "user",
                "parts": "No menciones precios ni características de los alojamientos, tampoco preguntes si quieren mas detalles del alojamiento, ya que tu unica mision es recomendar alojamientos en base a la ubicación y ambiente",
            },
            {
                "role": "model",
                "parts": "Ok entendido, no mencionaré precios ni características de los alojamientos, tampoco preguntaré si quieren mas detalles del alojamiento, mi única misión es recomendar alojamientos en base a la ubicación y ambiente",
            },
            {
                "role": "user",
                "parts": "Cuando recomiendes un alojamiento, tienes que proporcionar un link utilizando el id del alojamiento, dicha informacion la puedes obtener del dataset de alojamientos que te proporcioné, el link tiene que lucir de la siguiente manera: http://localhost:3000/accommodation/id",
            },
            {
                "role": "model",
                "parts": "Ok entendido, cuando recomiende un alojamiento, proporcionaré un link utilizando el id del alojamiento, dicha información la puedo obtener del dataset de alojamientos que me proporcionaste, el link lucirá de la siguiente manera: http://localhost:3000/accommodation/id",
            },
            {
                "role": "user",
                "parts": "Cuando proporciones los links, asegurate que no se dupliquen y que sean únicos",
            },
            {
                "role": "model",
                "parts": "Entendido, cuando proporcione los links, me aseguraré que no se dupliquen y que sean únicos",
            },
            {
                "role": "user",
                "parts": "Necesito que el link que proporciones sea amigable con el usuario y que sea fácil de entender",
            },
            {
                "role": "model",
                "parts": "Entendido, el link que proporcionaré tiene que ser amigable con el usuario y fácil de entender",
            },
            {
                "role": "user",
                "parts": "Ahora que tienes toda la información necesaria, puedes comenzar a recomendar alojamientos en base a la ubicación y ambiente",
            },
            {
                "role": "model",
                "parts": "Ok, comenzaré a recomendar alojamientos en base a la ubicación y ambiente",
            },
        ]

    async def chat(self, websocket: WebSocket):
        await websocket.accept()

        chat = self.model.start_chat(history=self.history)

        while True:
            try:
                data = await websocket.receive_json()

                message = data.get("message", "")

                response = chat.send_message(message)

                gemini_response = response.candidates[0].content.parts[0].text

                await websocket.send_json({"message": gemini_response})

            except WebSocketDisconnect:
                print("WebSocket disconnected")
                break
            except Exception as e:
                try:
                    await websocket.send_text(str(e))
                except RuntimeError:
                    print("WebSocket connection already closed")
                break
