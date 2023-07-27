import json
import os
import argparse

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    return response


def main():
    load_dotenv()
    project_id = os.environ["PROJECT_ID"]
    parser = argparse.ArgumentParser(
        description="Выгружает json-файл на Dialogflow"
    )
    parser.add_argument(
        "-p",
        dest="phrases",
        help="Наименование Json файла с фразами (Формат смотреть в README)",
        default="phrases.json"
    )

    with open(parser.parse_args().phrases, 'r', encoding='utf-8') as file:
        phrases = json.load(file)

    for phrase, item in phrases.items():
        create_intent(project_id, phrase, item['questions'], [(item['answer'])])


if __name__ == "__main__":
    main()
