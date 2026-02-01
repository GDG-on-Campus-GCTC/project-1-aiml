import torch
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import numpy as np

class ClipEncoder:
    def __init__(self):
        self.device = "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model.eval()
        self.model.to(self.device)

    def encode_image(self, image):
        """Encode image to embedding (returns 1D numpy array)"""
        if isinstance(image, Image.Image):
            if image.mode != 'RGB':
                image = image.convert('RGB')
        else:
            raise ValueError("Input must be PIL Image")
        
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            # Get image features - returns tensor of shape [1, embedding_dim]
            outputs = self.model.get_image_features(**inputs)
            # Remove batch dimension and convert to 1D numpy array
            return outputs[0].cpu().numpy()

    def encode_text(self, text):
        """Encode text to embedding (returns 1D numpy array)"""
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            # Get text features - returns tensor of shape [1, embedding_dim]
            outputs = self.model.get_text_features(**inputs)
            # Remove batch dimension and convert to 1D numpy array
            return outputs[0].cpu().numpy()
