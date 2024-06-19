import requests

url = "http://127.0.0.1:8000/run_srgan/"
data = {
    "image_path": "C:/Users/Admin/Desktop/GIS/SRGAN/SRGAN-Super-Resolution-GAN/Sentinel_TCI_cut.tif"
}

response = requests.post(url, json=data)
print(response)
