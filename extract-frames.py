import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'utterance': 'Whereas globalization has reduced global inequality (between nations), it has increased inequality within nations.',
    'package': 'propbank-grammar',
    'grammar': '*propbank-grammar*',
    'timeout': 100,
}

response = requests.post('http://127.0.0.1:1170/extract-frames', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"utterance":"Whereas globalization has reduced global inequality (between nations), it has increased inequality within nations.", "package": "propbank-grammar", "grammar": "*propbank-grammar*", "timeout": 100}'
#response = requests.post('http://127.0.0.1:1170/extract-frames', headers=headers, data=data)

print(response.text)