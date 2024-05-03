from seeq.sdk import LogsApi, ApiClient, AuthApi, AuthInputV1, LogMessage
import json

SEEQ_URL = '<seeq_base_url>'
SEEQ_USER_NAME = '<user name or access key>'
SEEQ_PASSWORD = '<password>' 

class LogMessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LogMessage):
            return {'timestamp': obj.time, 'source': obj.source, 'level': obj.level, 'message': obj.message}
        return super().default(obj)

def lambda_handler(event, context):
    return get_log_messages()

def get_log_messages():
    api_client = ApiClient(f'https://{SEEQ_URL}/api', None, None)
    auth_api = AuthApi(api_client)
    authInput = AuthInputV1(username=f'{SEEQ_USER_NAME}', password=f'{SEEQ_PASSWORD}')
    auth_api.login(body=authInput)
    logs_api = LogsApi(api_client)
    return json.dumps(logs_api.get_logs(log='jvm-link', limit=20, start_time='', end_time=''), cls=LogMessageEncoder)
