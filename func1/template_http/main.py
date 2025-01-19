import os
from google.cloud import storage
import functions_framework
# Add any imports that you may need, but make sure to update requirements.txt


@functions_framework.http
def create_text_file_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        Return the fileName in the body of the response.
        Return a HTTP status code of 200.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """

    request_json = request.get_json()

    bucket_name = os.getenv("BUCKET_ENV_VAR")

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    fileName = ""
    if "fileName" in request_json:
        fileName = request_json["fileName"]
    if "fileContent" in request_json:
        fileContent = request_json["fileContent"]

        with open(f"gs://{bucket_name}/{fileName}", "w") as file:
            file.write(fileContent)

    return "OK", f'{ "fileName":"{fileName}"}'
