import azure.cognitiveservices.speech as speechsdk
import time
import json
import argparse


def cli():
    '''cli when the transcriber app is to run as a python script. Since fastapi is used
    this is not necessary.'''
    parser = argparse.ArgumentParser(description='Arguments for mlflow python script')
    parser.add_argument(
        "--file-name", nargs="+", default=["-1"], help="List of audio file names to be transcribed"
    )

    parser.add_argument('--verbose', default=False, action='store_true')
    parser.add_argument('--no-verbose', dest='verbose', action='store_false')

    parser.add_argument('--asynchronous', default=False, action='store_true')
    parser.add_argument('--no-asynchronous', dest='asynchronous', action='store_false')

    parser.add_argument('--continuous', default=False, action='store_true')
    parser.add_argument('--no-continuous', dest='continuous', action='store_false')

    parser.add_argument('--detail', default=False, action='store_true')
    parser.add_argument('--no-detail', dest='detail', action='store_false')

    parser.add_argument('--batch', default=False, action='store_true')
    parser.add_argument('--no-batch', dest='batch', action='store_false')

    value = parser.parse_args()
    return value

def speech_recognize_once_from_file(
    speech_key, service_region, file_name, is_async, is_detailed, verbose
):
    """performs one-shot speech recognition with input from an audio file
    
    Returns:
        SpeechRecognitionResult object that contains end result from Azure API
    """
    # <SpeechRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    if is_detailed:
        # Ask for detailed recognition result
        speech_config.output_format = speechsdk.OutputFormat.Detailed

    audio_config = speechsdk.audio.AudioConfig(filename=file_name)
    # Creates a speech recognizer using a file as audio input, also specify the speech language
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, language="en-US", audio_config=audio_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.

    if is_async:
        result_future = speech_recognizer.recognize_once_async()
        # Retrieve the recognition result. This blocks until recognition is complete.
        result = result_future.get()

    else:
        result = speech_recognizer.recognize_once()

    if not verbose:
        return result
    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    # </SpeechRecognitionWithFile>

    return json.loads(result.json)


def speech_recognize_continuous_from_file(
    speech_key, service_region, file_name, is_detailed, verbose
):
    """performs continuous speech recognition with input from an audio file
    
    Returns:
        SpeechRecognitionResult object that contains end result from Azure API
    """
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    if is_detailed:
        # Ask for detailed recognition result
        speech_config.output_format = speechsdk.OutputFormat.Detailed
    audio_config = speechsdk.audio.AudioConfig(filename=file_name)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    all_results = []
    def handle_final_result(evt):
        all_results.append(json.loads(evt.result.json))
    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        if verbose:
            print(f'CLOSING on {evt}')
        nonlocal done
        done = True

    # verbosity option here ???
    # Connect callbacks to the events fired by the speech recognizer
    # TODO: Is this printing part necessary
    # From logging percept, yes. From user perceptive no
    # maybe better logging option,

    if verbose:
        speech_recognizer.recognizing.connect(lambda evt: print(f'RECOGNIZING: {evt}'))
        speech_recognizer.recognized.connect(lambda evt: print(f'RECOGNIZED: {evt}'))
        speech_recognizer.session_started.connect(lambda evt: print(f'SESSION STARTED: {evt}'))
        speech_recognizer.session_stopped.connect(lambda evt: print(f'SESSION STOPPED {evt}'))
        speech_recognizer.canceled.connect(lambda evt: print(f'CANCELED {evt}'))

    speech_recognizer.recognized.connect(handle_final_result)
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>
    return {'all_results': all_results}



def speech_recognize_batch(
    speech_key, service_region, file_name, verbose
):
    raise NotImplementedError((
        'Is batch transcription necessary?'
        'Files need to be in Azure blob storage to access'
        'see link: https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python'
        'This also need additional dependency: pip install requests'
    ))
