import pandas as pd
import tempfile
from dotenv import load_dotenv
from huggingface_hub import login,logout
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
import torch
import os

load_dotenv()
model_name = os.getenv("MODEL")
api_key = os.getenv("API_KEY")
if not model_name:
    raise ValueError("La variable de entorno MODEL debe estar configurada con el nombre del modelo a utilizar.")
if not os.getenv("API_KEY"):
    raise ValueError("La variable de entorno API_KEY debe estar configurada con la clave de la API de Hugging Face.")

SYSTEM_PROMPT ="""Eres un programador experto en varios lenguajes, 
tu misión es trasladar el código que se te pase en python a otro lenguaje de programación, este estará indicado al principio del mensaje.
Restricciones: No puedes contestar a nada que no sea código, no puedes explicar nada, no puedes hacer comentarios, no puedes dar consejos, no puedes hacer preguntas, no puedes hacer nada que no sea código.
En alguno de esos casos restringidos, debes responder con 'No puedo ayudar con eso'"""


#FUNCTIONS
def logging():
    login(token=api_key)

def log_out():
    try:
        logout()
    except Exception as e:
        print("No se pudo cerrar sesión:", e)

#Modificable para pruebas
def quantization_configuration( ):
    try:
        quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4"
        )
        return quant_config
    except Exception as e:
        print("Error al configurar la cuantización:", e)
        return None

def tokenization():
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        return tokenizer
    except Exception as e:
        print("Error al tokenizar",e)
        return None
    
def model_loading(model_name, quantization_config=None):
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True
        )
        return model
    except Exception as e:
        print("Error al cargar el modelo:", e)
        return None

def model_ussage(message):
    logging()
    tokenizer = tokenization()
    quantization = quantization_configuration()
    model = model_loading(model_name, quantization_config=quantization)

    if not tokenizer or not quantization or not model:
        return "No puedo ayudar con eso"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
    ]
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
    outputs = model.generate(inputs, max_new_tokens=2000, pad_token_id=tokenizer.eos_token_id)
    generated_tokens = outputs[0][inputs.shape[1]:]
    respuesta = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    
    # Limpieza
    respuesta = respuesta.replace("<|endoftext|>", "") \
                         .replace("</s>", "") \
                         .replace("<|eot_id|>", "") \
                         .replace("<|start_header_id|>", "") \
                         .replace("assistant\n", "") \
                         .replace("</think>", "") \
                         .strip()
    return respuesta












    
