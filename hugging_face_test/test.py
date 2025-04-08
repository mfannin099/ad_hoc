from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load pipeline (this was added by chatgpt and seemed to be the difference to make the script run)
if device == "cuda":
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
else:
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)

pipe = pipe.to(device)

print(pipe)
print("-------------------")
print('Begin Generating the image')

prompt = "a strong, but elegant, nerdy, goofy man in a business meeting"

image = pipe(prompt).images[0]

image.save("test.png")
