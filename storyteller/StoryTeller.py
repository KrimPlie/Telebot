import requests
import base64
import random
import pyttsx3


from gpt4all import GPT4All
from googletrans import Translator
# import torch



class StorryTeller():
    """
    Класс отвечающий за составление и отрисовку картинок для сказки
    prompt - первый промпт пользователя
    character_prompt - промпт для генерации персонажа
    max_tryies - максимальное количество глав
    """
    MAX_WORDS_IN_ANSWER = 300
    
    prev_story = None
    all_story = []
    all_images = []
    try_counter = 0
    
    def __init__(self, prompt:str, character_prompt:str=".", max_tryies:int=3) -> None:
        self.model = GPT4All(model_name="Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", model_path="model", device="kompute")
        self.translator = Translator()
        self.tts = pyttsx3.init()
        self.prompt = self.translate2en(prompt)
        self.character_prompt = self.translate2en(character_prompt)
        self.max_tryies = max_tryies
        
        
    def translate2ru(self, text:str):
        translated_text = self.translator.translate(text, src="en", dest="ru")
        return translated_text.text
    
    def translate2en(self, text:str):
        translated_text = self.translator.translate(text=text, src="ru", dest="en")
        return translated_text.text
        
    def generate_story(self, continue_prompt:str="da") -> str:
        """
        Генерирует начало/продолжение/конец сказки\n
        Для генерации глав нужно передать продолжение в continue_prompt
        """
        fairy_tale_starter_prompt = f"""You are a professional writer whose fairy tales are very popular with people of all ages.
                                    Your task is to write start of the best fairy tale in your life. This part should be short and ends in plot twist. 
                                    A fairy tale should be about:{continue_prompt}.
                                    Main chatacter in this fairu tale is {self.character_prompt}.
                                    You have to write ONLY a fairy tale and NOTHING more."""
                                    
        fairy_tale_countinuer_prompt = f"""You are a professional writer whose fairy tales are very popular with people of all ages.
                                        Your task is write the {self.try_counter}th of {self.max_tryies} parts of best fairy tale of your life.
                                        This part should be short and ends in plot twist.
                                        This story was about: {self.prompt}.
                                        Main chatacter in this fairu tale is {self.character_prompt}.
                                        You have to write ONLY a fairy tale and NOTHING more.
                                        Here are the previous actions in the fairy tale:"""
                                        
        fairy_tale_finisher_prompt = f"""You are a professional writer whose fairy tales are very popular with people of all ages.
                                    Your task is to write ending of the best fairy tale in your life. 
                                    The ending should be not long and have a logical final.
                                    A fairy tale was about: {self.prompt}.
                                    Main chatacter in this fairu tale is {self.character_prompt}.
                                    You have to write ONLY a fairy tale and NOTHING more.
                                    Here are the previous actions in the fairy tale:"""
                                        
        with self.model.chat_session():
            if self.prev_story == None:
                prompt = f"{fairy_tale_starter_prompt} {self.prompt}."
                print("Начало")
                
            elif self.try_counter < self.max_tryies-1: 
                prompt = f"{fairy_tale_countinuer_prompt} {self.prev_story}. The story should continue like this: {continue_prompt}"
                print("Середина")

            elif self.try_counter == self.max_tryies-1:
                prompt = f"{fairy_tale_finisher_prompt} {self.prev_story}."
                print("Конец")
            
            else:
                return "Сказка закончилась"
            
            self.prev_story = self.model.generate(prompt, max_tokens=self.MAX_WORDS_IN_ANSWER)
            
        
        self.try_counter += 1
        self.all_story.append(self.translate2ru(self.prev_story))
        return self.translate2ru(self.prev_story)
    
    def generate_image(self):
        """
        Позволяет получить изображение исходя из последней сгенерированной главы
        """
        prompt = self.prev_story.split(".")[0:2]
        prompt = " ".join(prompt)
        # print(prompt)
        body = {
                "prompt": f"fantasy, ({self.character_prompt}), {prompt}, colorful",
                "negative_prompt": "deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, disgusting, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, blurry, ((((mutated hands and fingers)))), watermark, watermarked, oversaturated, censored, distorted hands, amputation, missing hands, obese, doubled face, double hands",
                "seed": -1,
                "steps": 30,
                "width": 512,
                "height": 512,
                "cfg_scale": 8,
                "sampler_name": "DPM++ 2M",
                "n_iter": 1,
                "batch_size": 1
                }
        if self.try_counter <= self.max_tryies: 
            image = requests.post("http://localhost:7860/sdapi/v1/txt2img", json= body)
            image = image.json()["images"][0]
            img_name= f"temp/{random.randint(100000000,999999999)}_{prompt[:10].replace(' ','_').replace('.', '_').replace(',', '_')}.jpg"
            
            with open(img_name, "wb") as img:
                image_bytes = base64.b64decode(image)
                img.write(image_bytes)

                self.all_images.append(img_name)
                
            return img_name
        return "https://tenor.com/view/lets-go-gambling-gif-4822326163116896763"
    
    def get_all_story(self) -> list:
        """
        Возвращает список со всеми главами сказки
        """
        return self.all_story 
    
    def get_all_images(self) -> list:
        """
        Возвращает список со всеми картинками, сгенерированными в процессе создания сказки
        """
        return self.all_images

    def back(self) -> str:
        """
        Возвращает состояние сказки на главу назад
        """
        try:
            self.try_counter -= 1
            self.all_story.pop()
            self.prev_story = self.all_story[-1]
            return self.translate2ru(self.prev_story)
        except:
            return "Нечего отматывать STARE"
            
    def get_counter(self) -> int:
        return self.try_counter
    
    def get_tts(self) -> str:
        tts_name= f"temp/{random.randint(100000000,999999999)}_{self.prompt[:10].replace(' ','_').replace('.', '_').replace(',', '_')}.wav"
        self.tts.save_to_file(text=self.translate2ru(self.prev_story), filename=tts_name)
        self.tts.runAndWait()
        return tts_name
        
if __name__ == "__main__":


    pass
