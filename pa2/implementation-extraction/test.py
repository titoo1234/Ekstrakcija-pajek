import json 
      
# Data to be written 
dictionary ={ 
  "id": "04", 
  "name": "sunil", 
  "department": "HR",
  "items" : [{"ime":"telefon","cena":2},{"ime":"telefon2"},{"ime":"telefon3"}]
} 
      
# Serializing json  
json_object = json.dumps(dictionary, indent = 4) 
print(json_object)