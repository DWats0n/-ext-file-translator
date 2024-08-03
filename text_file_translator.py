from deep_translator import GoogleTranslator
import time
from tqdm import tqdm

max_litras_for_translate = 5000

#function for setting translater
def get_file_setting():
  flag = False
  file_path = str()
  while flag == False:
    file_path = input("wright file path\n->")
    try:
      open(file_path)
    except FileNotFoundError:
      print("File not found, try agine, please")
      continue
    flag = True
  file_name = file_path.split("\\")[-1]
  return file_path,file_name
  
def get_lenguch_to_translet():
  flag = False
  languch = str()
  while flag == False:
    languch = input("wright lenguch to translate(exempl: en, ru)\n->")
    if not GoogleTranslator().is_language_supported(language=languch):
      print("Sorry we can't supported this language")
      continue
    flag = True
  return languch

def get_users_setting():
  file_path,file_name = get_file_setting()
  languch = get_lenguch_to_translet()
  return [languch,file_path,file_name]

#function for translate file
def get_split(text:str, step=0):
  step_split = ["\n",".",","," "]
  
  if step > len(step_split)-1:
    return text
  
  fragments = []
  if step == 0:
    text = text.replace("\n","<\n>")
    step_split[0] = "<\n>"
  text_fragments = text.split(step_split[step])

  flag = False
  if text_fragments[-1] == "":
    text_fragments = text_fragments[:-1]
    flag = True
  
  for fragment_id in range(len(text_fragments)):
    if fragment_id != len(text_fragments)-1:
      fragments.append(text_fragments[fragment_id] + step_split[step])
    else:
      if flag:
        fragments.append(text_fragments[fragment_id] + step_split[step])
      else:
        fragments.append(text_fragments[fragment_id])

  fragment_id = 0
  while fragment_id < len(fragments):
    if len(fragments[fragment_id]) >= max_litras_for_translate:
      fragments = fragments[:fragment_id] + get_split(fragments[fragment_id],step=step+1) + fragments[fragment_id+1:]
      fragment_id = 0
      continue
    fragment_id += 1
    
  return fragments

def get_fragments(text:str):
  text_fragments = get_split(text)
  litras_count = 0
  fragments = []
  fragment = ""
  for text_fragment in text_fragments:
    litras_count += len(text_fragment)
    if litras_count < max_litras_for_translate:
      fragment += text_fragment
    else:
      fragments.append(fragment)
      litras_count = len(text_fragment)
      fragment = text_fragment
  fragments.append(fragment)

  return fragments

def translate_utilite(text : str, gt: GoogleTranslator):
  try:
    translate = gt.translate(text).replace("<\n>","\n")
  except Exception:
    translate = text
  return translate

def transletion_fragments(fragments : list, lenguch):
  translate = ""
  translater = GoogleTranslator(source='auto', target=lenguch)
  print("translation data")
  for fragmen in tqdm(fragments):
    translate += translate_utilite(fragmen, translater)
    
  return translate

def get_translate(setting:list):

  text = open(setting[1],"r",encoding="utf-8").read()
  
  fragments = get_fragments(text)
  
  translate = transletion_fragments(fragments, setting[0])
  
  return translate  

#function for wright in file_translate
def wright_translate_in_file(text,file_name):
  file_out_name = f"{file_name}_translate.txt"
  file_out = open(file_out_name,"w",encoding="utf-8")
  file_out.write(text)
  file_out.close()
  print(f"New file's name -> {file_out_name}")

#mine function
def __main__():
  setting = get_users_setting() 
  translate =  get_translate(setting)
  wright_translate_in_file(translate,setting[2])
  pass

__main__()
