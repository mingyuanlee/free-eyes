transcript_to_llm_input_prompt = """
You are a helpful assistant who is responsible for converting human voice to a generative AI model.
The Voice has been recorded as a transcript. 
Generate the input to llm, be sure to replace words that don't make sense in the context.
These words are recongized incorrectly by the speech recognition system and have similar sounds to the correct words.
Return only the transcript, no decorations or additional information.
This is the transcript: '''{}'''.
"""