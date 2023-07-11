import json
import os
import magic

import requests

print('💫 Starting uploading coverage report to Atena')
print('🔑Checking environment variables...')
print('🔑Checking upload key...')
if os.getenv('ATENA_API_KEY') is None or os.getenv('ATENA_API_KEY') == '':
    print('❌Failed: ATENA_UPLOAD_KEY is not set')
    exit(1)

key = os.getenv('ATENA_API_KEY')
url = os.getenv('ATENA_ENDPOINT')
version = os.getenv('VERSION')
artifact_path = os.getenv('ARTIFACT_PATH')
description = os.getenv('DESCRIPTION')
pre_release = os.getenv('PRE_RELEASE')

artifact_path = artifact_path.split(',')

for artifact in artifact_path:
    if not os.path.exists(artifact):
        print(f'❌Failed: {artifact} does not exist')
        exit(1)

print('✅Passed: Environment variables are set correctly')

form_data = {
    'version': version,
    'key': key,
    'description': description,
    'pre_release': pre_release
}

files = []
for artifact in artifact_path:
    files.append(('artifact', (os.path.basename(artifact), open(artifact, 'rb'), magic.from_file(artifact))))

print('📦Uploading artifacts...')
response = requests.post(url, data=form_data, files=files)
output = response.text

if response.status_code != 201:
    output = json.loads(output)
    print(f'✅ Successfully create a release on {output["repository"]} with ID {output["release_id"]}')
    print(f'Full response: {response.text}')
    exit(0)
else:
    print(f'❌Failed: {response.text}')
    exit(1)
