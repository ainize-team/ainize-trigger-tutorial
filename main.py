import os
import json
import logging
import asyncio
import torch
from ain.ain import Ain
from flask import Flask, request
from ain.types import ValueOnlyTransactionInput
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# load model, tokenizer
model = GPT2LMHeadModel.from_pretrained('./GPT2-PrideAndPrejudice')
tokenizer = GPT2Tokenizer.from_pretrained('./GPT2-PrideAndPrejudice')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# connect node
PROVIDER_URL = os.environ['PROVIDER_URL']
AINIZE_INTERNAL_PRIVATE_KEY = os.environ['AINIZE_INTERNAL_PRIVATE_KEY']
ain = Ain(PROVIDER_URL, chainId=0)
ain.wallet.addAndSetDefaultAccount(AINIZE_INTERNAL_PRIVATE_KEY)

# ain-py
loop = asyncio.get_event_loop()

# flask
app = Flask(__name__)

async def set_value(ref, value):
    result = await ain.db.ref(ref).setValue(
        ValueOnlyTransactionInput(
            value=value,
            nonce=-1
        )
    )

def make_story(base_text, length):
    try:
        # Encoding of input text
        input_ids = tokenizer.encode(base_text, return_tensors='pt')
        # Both input and model must use the same device (cpu or gpu)
        input_ids = input_ids.to(device)
        # Generate prediction
        outputs = model.generate(input_ids, pad_token_id=50256,
                                 do_sample=True,
                                 max_length=length,
                                 top_k=40,
                                 num_return_sequences=1)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result

    except Exception as e:
        logging.error(f'Error occur in script generating : {e}')

@app.route('/trigger', methods=['POST'])
def trigger():
    res = json.loads(request.data.decode('utf-8'))
    if (not res.get('transaction') or
            not res['transaction'].get('tx_body') or
            not res['transaction']['tx_body'].get('operation')):
        return f'Invalid transaction : {res}', 400
    transaction = res['transaction']['tx_body']['operation']
    tx_type = transaction['type']
    if tx_type != 'SET_VALUE':
        return f'Not supported transaction type : {tx_type}', 400
    value = eval(transaction['value'])
    result = make_story(value['baseText'], value['len'])
    try:
        result_ref = transaction['ref'].split('/')[:-1]
        result_ref.append('result')
        result_ref = '/'.join(result_ref)
        loop.run_until_complete(set_value(result_ref, result))
    except Exception as e:
        logging.error(f'setValue failure : {e}')
        return f'setValue failure : {e}', 500
    return '', 204


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')
