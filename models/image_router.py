class ImageRouter:

    def __init__(self):

        self.supported_images = {
            "chest": "Chest X-ray",
            "x-ray": "Chest X-ray",
            "lung": "Chest X-ray",
            "brain": "Brain MRI",
            "mri": "Brain MRI",
            "eye": "Eye Fundus",
            "retina": "Eye Fundus",

    # Chest X-ray
    "chest": "Chest X-ray",
    "x-ray": "Chest X-ray",
    "xray": "Chest X-ray",
    "lung": "Chest X-ray",
    "lungs": "Chest X-ray",
    "thorax": "Chest X-ray",

    # Brain MRI
    "brain": "Brain MRI",
    "mri": "Brain MRI",
    "brain scan": "Brain MRI",

    # Eye Fundus
    "eye": "Eye Fundus",
    "retina": "Eye Fundus",
    "retinal": "Eye Fundus",
    "fundus": "Eye Fundus",
    "optic disc": "Eye Fundus",
    "macula": "Eye Fundus"
        }

    def detect_image_type(self, caption):

        caption = caption.lower()

        for keyword, image_type in self.supported_images.items():

            if keyword in caption:

                return image_type

        return "General Medical Image"