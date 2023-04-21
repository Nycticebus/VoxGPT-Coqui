# VoxGPT-Coqui

This is a web app that gives ChatGPT a realistic voice interface. 

Here's a video with no editing: 

OpenAI Whisper is used for speech-to-text, OpenAI `gpt-3.5-turbo`/`gpt-4` for completion, and Coqui TTS for voice synthesis. 

It's a fork of the VoxGPT repo here: https://github.com/lspahija/VoxGPT

Coqui TTS: https://github.com/coqui-ai/TTS

To get it running:  
1. `git clone git@github.com:Nycticebus/VoxGPT-Coqui.git`
2. `cd VoxGPT-Coqui`
3. `mkdir env && cd env` 
4. `echo "OPENAI_API_KEY={YOUROPENAIAPIKEY}" >> openai-api-key` where {YOUROPENAIAPIKEY} is your openAI API Key, found at https://platform.openai.com/account/api-keys
5. `docker build -t voxgpt-coqui .`
6. `docker run -d -p 8001:80 --gpus all --env-file ./env/openai-api-key voxgpt-coqui`
7. navigate to `localhost:8001` in a modern browser

The AI model defaults to `gpt-3.5-turbo` but you can adjust this by setting the `AI_COMPLETION_MODEL` environment variable (e.g. to `gpt-4` if your `OPENAI_API_KEY` has access to it)

You can configure the language by setting the `LANGUAGE` environment variable to the corresponding ISO-639-1 code. The default is `en`. The supported languages are:

- af: Afrikaans
- ar: Arabic
- bg: Bulgarian
- bn: Bengali
- bs: Bosnian
- ca: Catalan
- cs: Czech
- da: Danish
- de: German
- el: Greek
- en: English
- es: Spanish
- et: Estonian
- fi: Finnish
- fr: French
- gu: Gujarati
- hi: Hindi
- hr: Croatian
- hu: Hungarian
- id: Indonesian
- is: Icelandic
- it: Italian
- iw: Hebrew
- ja: Japanese
- jw: Javanese
- km: Khmer
- kn: Kannada
- ko: Korean
- la: Latin
- lv: Latvian
- ml: Malayalam
- mr: Marathi
- ms: Malay
- my: Myanmar (Burmese)
- ne: Nepali
- nl: Dutch
- no: Norwegian
- pl: Polish
- pt: Portuguese
- ro: Romanian
- ru: Russian
- si: Sinhala
- sk: Slovak
- sq: Albanian
- sr: Serbian
- su: Sundanese
- sv: Swedish
- sw: Swahili
- ta: Tamil
- te: Telugu
- th: Thai
- tl: Filipino
- tr: Turkish
- uk: Ukrainian
- ur: Urdu
- vi: Vietnamese
- zh: Chinese (Mandarin)