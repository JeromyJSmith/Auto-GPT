import hashlib
import os
import unittest

from PIL import Image

from autogpt.commands.image_gen import generate_image, generate_image_with_sd_webui
from autogpt.config import Config
from autogpt.workspace import path_in_workspace
from tests.utils import requires_api_key


def lst(txt):
    return txt.split(":")[1].strip()


@unittest.skipIf(os.getenv("CI"), "Skipping image generation tests")
class TestImageGen(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    @requires_api_key("OPENAI_API_KEY")
    def test_dalle(self):
        self.config.image_provider = "dalle"

        # Test using size 256
        result = lst(generate_image("astronaut riding a horse", 256))
        image_path = path_in_workspace(result)
        self.assertTrue(image_path.exists())
        with Image.open(image_path) as img:
            self.assertEqual(img.size, (256, 256))
        image_path.unlink()

        # Test using size 512
        result = lst(generate_image("astronaut riding a horse", 512))
        image_path = path_in_workspace(result)
        with Image.open(image_path) as img:
            self.assertEqual(img.size, (512, 512))
        image_path.unlink()

    @requires_api_key("HUGGINGFACE_API_TOKEN")
    def test_huggingface(self):
        self.config.image_provider = "huggingface"

        # Test usin SD 1.4 model and size 512
        self.config.huggingface_image_model = "CompVis/stable-diffusion-v1-4"
        result = lst(generate_image("astronaut riding a horse", 512))
        image_path = path_in_workspace(result)
        self.assertTrue(image_path.exists())
        with Image.open(image_path) as img:
            self.assertEqual(img.size, (512, 512))
        image_path.unlink()

        # Test using SD 2.1 768 model and size 768
        self.config.huggingface_image_model = "stabilityai/stable-diffusion-2-1"
        result = lst(generate_image("astronaut riding a horse", 768))
        image_path = path_in_workspace(result)
        with Image.open(image_path) as img:
            self.assertEqual(img.size, (768, 768))
        image_path.unlink()

    def test_sd_webui(self):
        self.config.image_provider = "sd_webui"
        return


if __name__ == "__main__":
    unittest.main()
