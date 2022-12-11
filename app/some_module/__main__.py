import os

from .transcription import (
    speech_recognize_once_from_file,
    speech_recognize_batch,
    speech_recognize_continuous_from_file,
    cli
)

SPEECH_KEY = os.environ.get('SPEECH_KEY')

SPEECH_REGION = os.environ.get('SPEECH_REGION')

def transcribe_speech(
    file_name, is_async, is_continuous, is_detailed, is_batched, verbose=False
):  
    '''
    Ultimate function to transcribe speech
    
    Args:

        file_name (str):
            file_name audio file to be transcribed.

        is_async (bool):
            whether to run asynchrounous speech reconition or not

        is_continuous (bool):
            whether to run asynchrounous speech reconition or not

        is_detailed (bool):
            Whether output should be detailed or not

        is_batched:
            If true, runs batched version of Azure Speech Recognition

    Returns:
        SpeechRecognitionResult object that contains end result from Azure API
    '''
    # Ultimate function to transcribe speech

    if is_batched:
        speech_recognize_batch(SPEECH_KEY, SPEECH_REGION, file_name, verbose)

    if is_continuous:
        return speech_recognize_continuous_from_file(
            SPEECH_KEY, SPEECH_REGION, file_name, is_detailed, verbose
        )

    return speech_recognize_once_from_file(
        SPEECH_KEY, SPEECH_REGION, file_name, is_async, is_detailed, verbose
    )



if __name__ == '__main__':
    
    # audio_file = 'sample1.wav'
    cli_args = cli()
    file_name_arr = [cli_args.file_name] if isinstance(cli_args.file_name, str) else cli_args.file_name

    for file_name in file_name_arr:
        print(f'Transcribing {file_name}')
        transcribe_speech(
            file_name, cli_args.asynchronous, cli_args.continuous,
            cli_args.detail, cli_args.batch, cli_args.verbose
        )
