FINE_TUNE_CURIE_MODEL = "curie:ft-personal:first-fine-tuning-2022-09-10-15-06-54"
STANDRD_DAVINCI_MODEL = "text-davinci-002"

standard_config = {
    "model": STANDRD_DAVINCI_MODEL,
    "temp": 0.2,
    "top_p": 1.0,
    "max_tokens": 27
}


finetuned_config = {
    "model": FINE_TUNE_CURIE_MODEL,
    "temp": 0.2,
    "top_p": 1.0,
    "max_tokens": 27,
    "stop": ["\n"]
}
