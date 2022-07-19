import requests

def requestBetaTransfer(method, data):
    public_key = 'tpSnYI4yxJTM1OdQqr9RCDeUvl2hFsWE'
    secret_key= 'yH8mPYiqAsDvxWoIlSdFKVbTn02XOaJQ'

    url = 'https://merchant.betatransfer.io/api/{method}?{data}'.format(method, data);

    requests.get(url)