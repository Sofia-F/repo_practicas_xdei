
import base64
import math

# with open('product1.jpg', 'rb') as file:
#     data = file.read()

# enc_data_wo_pad = base64.b64encode(data).decode('utf-8').rstrip('=')

# enc_data_w_pad = enc_data_wo_pad.ljust(math.ceil(len(enc_data_wo_pad) / 4) * 4, '=')
# print(enc_data_w_pad)


def b64(data):        
    with open(data, 'rb') as file:
        img = file.read()

    enc_data_wo_pad = base64.b64encode(img).decode('utf-8').rstrip('=')

    enc_data_w_pad = enc_data_wo_pad.ljust(math.ceil(len(enc_data_wo_pad) / 4) * 4, '=')
    return enc_data_w_pad

print(b64('product1.jpg'))