INPUT_SUFFIX = "write 3 emotions and 3 keywords, both analyzed from the text, in this format:\n" \
              "\"emotions\": 3 emotions\n" \
              "\"keywords\": 3 keywords"

PROMPT_END_SUFFIX = "\n###"


config = {
    "model": "text-davinci-002",
    "temp": 0.2,
    "top_p": 1.0,
    "max_tokens": 150,
    "stop": ["###"]
}
