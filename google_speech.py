from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import os
import json


CREDITIONALS_JSON = 'steady-cat-269313-8b90bcfb5b51.json'


def recognize(storage_uri, creditionals_json=None, language_code="en-US", sample_rate_hertz=24000):
    """
    Performs synchronous speech recognition on an audio file

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
      language_code The language of the supplied audio
      creditionals_json path to server account json file
      sample_rate_hertz Sample rate in Hertz of the audio data sent
    """

    if creditionals_json:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creditionals_json

    client = speech_v1p1beta1.SpeechClient()
    language_code = language_code
    sample_rate_hertz = sample_rate_hertz

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "enable_word_time_offsets": True,
    }
    audio = {"uri": storage_uri}

    # response = client.recognize(config, audio)
    operation = client.long_running_recognize(config, audio)
    response = operation.result()
    json_result = dict()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        # print(f"Transcript: {alternative.transcript}")

        json_result['transcript'] = alternative.transcript
        json_result['confidence'] = alternative.confidence
        json_result['language_code'] = language_code
        json_result['sample_rate_hertz'] = sample_rate_hertz
        json_result['words'] = list()

        for word in alternative.words:
            # print(f"Word: {word.word}")
            # print(f"Start time: {word.start_time.seconds} seconds {word.start_time.nanos} nanos")
            # print(f"End time: {word.end_time.seconds} seconds {word.end_time.nanos} nanos")

            json_result['words'].append({'word': word.word,
                                         'start_time': word.start_time.seconds + word.start_time.nanos / 1000**3,
                                         'end_time': word.end_time.seconds + word.end_time.nanos / 1000**3
                                         })

    # print(f'RESPONSE:   {json_result}')

    json_result = json.dumps(json_result)
    return json_result


if __name__ == '__main__':
    uri = 'gs://subtitles-a6e05.appspot.com/test.mp3'
    print(recognize(uri, CREDITIONALS_JSON))
