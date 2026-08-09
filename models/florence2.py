from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch


class FlorenceModel:

    def __init__(self):

        self.model_name = "microsoft/Florence-2-base"

        print("Loading Florence-2...")

        self.processor = AutoProcessor.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model.eval()

        print("Florence-2 Loaded Successfully!")

    def generate_caption(self, image: Image.Image):

        # Fast resize for high-speed CPU inference
        small_image = image.copy()
        small_image.thumbnail((512, 512))

        prompt = "<CAPTION>"

        inputs = self.processor(
            text=prompt,
            images=small_image,
            return_tensors="pt"
        )

        with torch.no_grad():

            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=40,
                do_sample=False
            )

        generated_text = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=False
        )[0]

        result = self.processor.post_process_generation(
            generated_text,
            task=prompt,
            image_size=image.size
        )

        return result

    def ask_question(self, image: Image.Image, question: str):

        prompt = "<VQA>" + question

        inputs = self.processor(
            text=prompt,
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():

            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=128
            )

        generated_text = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=False
        )[0]

        result = self.processor.post_process_generation(
            generated_text,
            task="<VQA>",
            image_size=image.size
        )

        return result