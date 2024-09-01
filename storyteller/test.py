import requests
def generate_image(self=0):
        # prompt = self.prev_story.split("\n")[0]
        # print(prompt)
        prompt = "Fraiki returned to the village, but something was different this time. The once vibrant streets were now silent and abandoned. Every house stood empty, windows boarded up as if hiding from an unseen threat. Confused and alarmed, Fraiki approached the village square where he had spent countless joyous days with his friends."
        body = {
                "prompt": f"fantasy, {prompt}, colorful",
                "negative_prompt": "deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, disgusting, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, blurry, ((((mutated hands and fingers)))), watermark, watermarked, oversaturated, censored, distorted hands, amputation, missing hands, obese, doubled face, double hands",
                "seed": -1,
                "steps": 20,
                "width": 512,
                "height": 512,
                "cfg_scale": 7,
                "sampler_name": "DPM++ 2M",
                "n_iter": 1,
                "batch_size": 1
                }
        image = requests.post("http://localhost:7860/sdapi/v1/txt2img", json= body)
        return image.json()["images"][0]

print(generate_image())