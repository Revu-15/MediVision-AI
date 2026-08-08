class ImageRouter:

    def __init__(self):

        self.supported_images = {
            "chest": "Chest X-ray",
            "x-ray": "Chest X-ray",
            "lung": "Chest X-ray",
            "brain": "Brain MRI",
            "mri": "Brain MRI",
            "skin": "Skin Image",
            "dermatology": "Skin Image",
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

    # Skin
    "skin": "Skin Disease",
        "lesion": "Skin Disease",
        "rash": "Skin Disease",
        "mole": "Skin Disease",
        "dermatology": "Skin Disease",
        "dermis": "Skin Disease",
        "psoriasis": "Skin Disease",
        "eczema": "Skin Disease",
        "acne": "Skin Disease",
        "wart": "Skin Disease",
        "blister": "Skin Disease",
        "fungal": "Skin Disease",
        "infection": "Skin Disease",
        "pigmented": "Skin Disease",
        "melanoma": "Skin Disease",
        "nevus": "Skin Disease",
        "arm": "Skin Disease",
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

        return "Unknown"