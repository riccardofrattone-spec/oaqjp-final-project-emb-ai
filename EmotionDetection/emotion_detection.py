"""Analyze English text using the IBM Skills Network Watson service."""

import json
import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the highest-scoring emotion.

    Watson's HTTP 400 response represents invalid or blank input and
    produces a dictionary containing None for every result field.
    Service and transport failures propagate for the caller to handle.
    """
    response = requests.post(
        EMOTION_URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers={
            "grpc-metadata-mm-model-id":
                "emotion_aggregated-workflow_lang_en_stock"
        },
        timeout=30,
    )
    if response.status_code == 400:
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    response.raise_for_status()
    payload = json.loads(response.text)
    scores = payload["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
