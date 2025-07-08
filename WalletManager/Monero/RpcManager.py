import requests
from requests.auth import HTTPDigestAuth

class WalletRPC:
    def __init__(self, host='monero-wallet-rpc', port=18082, user="pup", passwd="pup"):
        self.url = f'http://{host}:{port}/json_rpc'
        self.headers = {'Content-Type': 'application/json'}
        self.user = user
        self.passwd = passwd

    def create_address(self, label=None):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "create_address",
            "params": {
                "account_index": 0,
                "label": label if label is not None else "USER_ADDRESS"
            }
        }
        response = requests.post(self.url, json=payload, headers=self.headers, auth=HTTPDigestAuth(self.user, self.passwd))
        response.raise_for_status()
        return response.json().get("result", {})

    def list_subaddresses(self):

        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_address",
        }
        response = requests.post(self.url, json=payload, headers=self.headers, auth=HTTPDigestAuth(self.user, self.passwd))
        response.raise_for_status()
        return response.json().get("result", {}).get("addresses", [])

    def get_balance(self, address: int):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_balance",
            "params": {
                "account_index": 0,
                "address_indices": [address]
            }
        }

        response = requests.post(
            self.url,
            json=payload,
            headers=self.headers,
            auth=HTTPDigestAuth(self.user, self.passwd)
        )
        response.raise_for_status()
        result = response.json().get("result", {})

        simplified = []
        for entry in result.get("per_subaddress", []):
            simplified.append({
                "index": entry.get("address_index"),
                "label": entry.get("label"),
                "balance": entry.get("balance"),
                "unlocked_balance": entry.get("unlocked_balance")
            })

        return simplified

    def transfer(self, subaddr_index, destination, amount, priority=0):        # Validate priority
        if priority not in range(0, 5):
            raise ValueError("Priority must be between 0-4")

        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "transfer",
            "params": {
                "destinations": [{
                    "amount": int(amount * 1e12),  # Monero uses atomic units (piconeros)
                    "address": str(destination)
                }],
                "subaddr_indices": [int(subaddr_index)],
                "priority": int(priority)
            }
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                auth=HTTPDigestAuth(self.user, self.passwd),
                timeout=10
            )
            response.raise_for_status()
            json_response = response.json()

            # Check for RPC-level errors
            if "error" in json_response:
                raise RuntimeError(f"RPC error: {json_response['error']}")

            return json_response.get("result", {})

        except requests.exceptions.RequestException as e:
            # Handle network/HTTP errors
            raise ConnectionError(f"Request failed: {str(e)}")

# Example usage:
# rpc = WalletRPC()
# rpc.create_subaddress(0, label='Savings')
# rpc.list_subaddresses(0)
# rpc.make_transaction_from_subaddress(0, 1, '44AFFq5kSiGBoZ...', 0.5)
