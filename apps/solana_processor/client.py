import requests

def json_rpc_call(method, params):
    url = "http://localhost:5000"
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    # url = "https://magiceden.io/item-details/DGyXPsvrcJjZW93ktoC1XkLqUDyVitEgpN7dXtTC8JPD?name=TOLY"

    result = json_rpc_call("process", {
        "url": "https://magiceden.io/item-details/DGyXPsvrcJjZW93ktoC1XkLqUDyVitEgpN7dXtTC8JPD?name=TOLY"
    })
    print("Result of process:", result)

    # result = json_rpc_call("subtract", {"a": 10, "b": 4})
    # print("Result of subtract:", result["result"])
