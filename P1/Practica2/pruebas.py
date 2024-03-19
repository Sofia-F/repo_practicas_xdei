
import base64
import math

with open('product1.jpg', 'rb') as file:
    data = file.read()

enc_data_wo_pad = base64.b64encode(data).decode('utf-8').rstrip('=')

enc_data_w_pad = enc_data_wo_pad.ljust(math.ceil(len(enc_data_wo_pad) / 4) * 4, '=')
