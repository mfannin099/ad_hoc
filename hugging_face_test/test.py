from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)
print(pipe)
# prompt = "a strong, but elegant man saving the day"
# image = pipe(prompt).images[0]  
    
# image.save("test.png")

## oof

## Testing the visual studio commit