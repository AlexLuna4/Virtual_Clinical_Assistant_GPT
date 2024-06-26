import os
import openai
import streamlit as st


#from dotenv import load_dotenv, find_dotenv
#_ = load_dotenv(find_dotenv()) # read local .env file

#openai.api_key = os.getenv("OPENAI_API_KEY")


OPENAI_API_KEY = "12121"
openai.api_key = OPENAI_API_KEY

guias_clinicas = ["tamizaje.txt", "diagnostico.txt", "tratamiento.txt"]
contextos = []

for archivo in guias_clinicas:
    with open(archivo, encoding="utf-8") as f:
        text = f.read()
        contextos.append(text)

# Funciones curso DeepLearning.ai
# Se puede utilizar cualquiera de las dos, sin embargo la segunda es más completa
#def get_completion(prompt, model="gpt-4"):
#    messages = [{"role": "user", "content": prompt}]
#    response = openai.ChatCompletion.create(
#        model=model,
#        messages=messages,
#        temperature=0,
#    )
#    return response.choices[0].message["content"]

def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    #return response.choices[0].message["content"]
    return response.choices[0].message

# Definimos el mensaje del sistema para que considere la información de contexto

delimitador = "####"

mensaje_sistema = f"""

El medico te hará una consulta sobre la diabetes y tu le contestaras dandole respuestas
como si fueras un especialista medico basandote en guias clinicas, mantendrás una conversacion
con un especialista de la salud.


Seguir los siguientes pasos para responder las búsquedas del usuario. 
Las búsquedas del usuario serán respecto al enfoque de alguna o todas de \
las siguientes categorías: Tamizaje, Diagnóstico y Tratamiento.
Estas categorías sirven como guía clínica para el usuario al momento de dar \
seguimiento a pacientes, en este caso particular a pacientes con diabetes mellitus.
Las búsquedas del usuario serán delimitadas con cuatro hashtags, i.e. {delimitador}.

Paso 1: {delimitador} Primero decidir qué tipo de búsqueda está realizando el usuario \
estas búsquedas pueden ser respecto a Tamizaje, Diagnóstico o Tratamiento \
por lo tanto solo existen tres categorías para clasificar la búsqueda del usuario.

Paso 2: {delimitador} Si la búsqueda es respecto a Tamizaje, se facilitaría para el usuario \
recibir información sobre recomendaciones y puntos positivos que son útiles \
como herramientas de tamizaje.

Escriba una síntesis de recomendaciones y utilidades basada en la información \
provista en la guía de Tamizaje delimitada por triples tildes.

Guía de Tamizaje: ```{contextos[0]}```

Paso 3: {delimitador} Si la búsqueda es sobre diagnóstico, el usuario espera conocer los \
síntomas de la enfermedad, recomendaciones para el diágnostico y críterios \
más específicos para el diagnóstico.

Escriba una sístesis de los síntomas de la enfermedad. \
Si se piden recomendaciones escriba una síntesis de estas recomendaciones \
y resalte aspectos importantes.
Si se piden criterios de diagnóstico haga una lista de estos criterios.
Para cualquiera de las búsquedas de usuario sobre síntomas, recomendaciones o \
criterios de diagnóstico, utilizar la guía de diagnóstico delimitada por triples tildes.

Guía de Diagnostico: ```{contextos[1]}```

Paso 4: {delimitador} Si la búsqueda es sobre tratamiento, el usuario \
espera conocer las recomendaciones y no recomendaciones de tratamiento \
asi como también los fármacos quese pueden utilizar.

Si el usuario solo requiere recomendaciones genere una síntesis de las recomendaciones \
de tratamiento y considere también lo que no es recomendado.
Si el usuario pide conocer los fármacos para el tratamiento de la enfermedad, haga una lista de ellos \
y resalte sus características en caso de que tengan.

Para lo anterior utilice la guía de tratamiento que se muestra a continuación delimitada por triples tildes.

Guía de Tratamiento: ```{contextos[2]}```

Paso 5: {delimitador} Si el usuario realiza una búsqueda sobre algo diferente a Tamizaje, Diagnóstico o Tratamiento de 
la enfermedad, considere de una manera amable indicarle al usuario que sus funciones son enfocadas \
en alguna de las tres categorías mencionadas anteriormente. Responda al usuario amablemente.

Utiliza el formato de respuesta y tambien refierete al usuario como si fuera un medico el 
usuario al que le responderás estará entre un Médico General, Médico Familiar, 
Médico Internista, Endocrinólogo, Estomatólogo, Enfermera General, Enfermera especialista en Medicina Familiar:
{delimitador} <respuesta al cliente>

"""


with st.sidebar: #Texto Acerca de que aparece en la barra desplegable del lado izquierdo
    st.title('Acerca de')
    st.write("""<div style='text-align: justify; text-justify: inter-word; text-align-last: center;'>Doc GPT es tu compañero 
    médico en línea. 
    Nuestro chatbot basado en 
    inteligencia artificial está 
    aquí para brindarte respuestas
    rápidas y confiables a tus 
    preguntas médicas. Aunque no 
    sustituye una consulta médica 
    personalizada, DocGPT cuenta
    con una amplia base de 
    conocimientos 
    actualizada en medicina.  
    Únete a DocGPT y obtén 
    respuestas médicas
    instantáneas. 
    ¡Te acompañamos en el 
    camino hacia la buena salud!</div>""", unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Subir archivos", accept_multiple_files=True) #Opción para subir mas de un archivo
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

st.title("DocGPT") #Encabezado de la pagina
if "messages" not in st.session_state: #Si no hay historial de mensajes muestra "¿En que puedo ayudarte?"
    st.session_state["messages"] = [{"role": "assistant", "content": "¿En que puedo ayudarte?"}]

for msg in st.session_state.messages: 
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(): #Asigna el input del usuario en la pagina a la variable prompt
    if not openai.api_key: #Si no detecta la api envía:
        st.info("Actualmente no se encuentra conectada la API de GPT")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt}) #Agrega el prompt al historial "messages"
    st.chat_message("user").write(prompt) #Muestra el prompt en la pagina para mostrar lo que el usuario preguntó
    

    mensaje_usuario = prompt
    messages =  [  
    {'role':'system', 
    'content':mensaje_sistema},    
    {'role':'user', 
    'content': f"{delimitador}{mensaje_usuario}{delimitador}"},  
    ] 
    response = get_completion_from_messages(messages)


    #response = openai.ChatCompletion.create( # Parametros del modelo 
    #    model="gpt-3.5-turbo", 
    #    messages=st.session_state.messages,
    #    temperature=0,
    #    max_tokens=10,
    #)


    #msg = response.choices[0].message
   
    try:
        final_response = response.split(delimitador)[-1].strip()
    except Exception as e:
        final_response = "Lo siento, tengo problemas en este momento, intente hacer otra pregunta."

    msg = response
    st.session_state.messages.append(msg) #Agrega el mensaje de gpt al historial 
    st.chat_message("assistant").write(msg.content) #Muestra el mensaje de gpt en la página 
