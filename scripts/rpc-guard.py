"""Optional live RPC identity check. Does not deploy, sign, or use credentials."""
import json
import urllib.request

RPC='https://studio.genlayer.com/api'
BODY=json.dumps({'jsonrpc':'2.0','id':1,'method':'eth_chainId','params':[]}).encode()
req=urllib.request.Request(RPC, data=BODY, headers={
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'paretorail-network-guard/1.0',
})
with urllib.request.urlopen(req,timeout=12) as response:
    result=json.load(response)
if 'error' in result: raise SystemExit(f'RPC error: {result["error"]}')
chain=int(result['result'],16)
if chain != 61999:
    raise SystemExit(f'WRONG_CHAIN {chain}; expected 61999')
print('Confirmed StudioNet chain 61999 from',RPC)
