#Note: This code sample requires OpenAI Python library version 1.x.
from decouple import config # env vars
import time
import openai

def generate_map_icon(input):
    # LAYER 1
    client = openai.AzureOpenAI(
        # This is the default and can be omitted
        api_key=config("OPENAI_API_KEY"),
        api_version="2024-12-01-preview",
        azure_endpoint="https://openai-tidehackathon2025.openai.azure.com/",
    )
    
    prompt = """
    based on the instructions that follow, produce a json object exactly like this:
    {"latitude": lat, "longitude": lon, "iconName": iconName} 
    where lat and lon are the coordinates of the location you were given in the instructions.
    icon name possibilities are tankIcon, trainIcon. 
    your result should contain nothing but the intended json object. do not include any other text or explanation
    instructions:
    """

    chat_completion1 = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt + input
            }
        ],
        model="gpt-4o",
    )

    gpt_layer1 = chat_completion1.choices[0].message.content

    # contains chatgptese output strings
    print(gpt_layer1)
    return gpt_layer1

def generate_instruction_object(input):
    # LAYER 1
    client = openai.AzureOpenAI(
        # This is the default and can be omitted
        api_key=config("OPENAI_API_KEY"),
        api_version="2024-12-01-preview",
        azure_endpoint="https://openai-tidehackathon2025.openai.azure.com/",
    )
    
    prompt = """
    From the instructions that follow, supply the coordinates of the start point,
    end point, and type of object, in the following format:
    
    {'Object_Type' : type,
        'StartLat': lat,
        'StartLong': long,
        'EndLat': lat,
        'EndLong': long,
        }

    the object type can be either 'Tank','Land','Troops','Light Vehicle', "Boat", "Truck", 'Rail','Train','Wagon'
    If you don't know, default to "Truck". make sure it's returned in quotes.
    do not return anything in your response other than what's in curly brackets.
    instructions:
    """

    chat_completion1 = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt + input
            }
        ],
        model="gpt-4o",
    )


    gpt_layer1 = chat_completion1.choices[0].message.content

    # contains chatgptese output strings
    print("gpt response: " + gpt_layer1)
    return gpt_layer1

if __name__== "__main__":
    # generate_text_content("Get the coordinates of Ottawa.")
    t0 = time.time()
    generate_instruction_object("Tank movements spotted on the road from Hanover to Bergen")
    t1 = time.time()
    print("Done in " + str(t1 - t0) + " seconds")