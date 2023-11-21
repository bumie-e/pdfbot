import streamlit as st
from streamlit_chat import message
from pdfquery import generate_response, uploadFile
from translate import translate_lang


# Setting page title and header
st.set_page_config(page_title="PDF Bot", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>PDF Bot - Query any pdf! </h1>", unsafe_allow_html=True)

st.write('Supports African local langugage too!')

target_language = st.radio(
    "Select your preferred Langugage",
    ["English", "French :flag-fr:", "Yoruba :flag-ng:", "Igbo :flag-ng:", "Hausa :flag-ng:", "Swahili" "Spanish :flag-es:" ],
    )

prompt = '' # User defined


# Set up the header information, which includes our subscription key


# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": f"Hello"}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []


# Sidebar - Add new pdf files for querying or clear the whole conversation
st.sidebar.title("Settings")

filepath = st.sidebar.text_area("Enter the file directory")
if st.sidebar.button('Upload new files'):
    uploadFile(filepath)

clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": f"Hello"}
    ]
    # st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []



# generate a response
def request(prompt, target_language='en'):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    response = generate_response(prompt)
    
    if target_language !='English':
            response = translate_lang(target_language, response)

    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response

st.markdown('<h3> Chat </h3>', unsafe_allow_html=True)

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = request(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
       
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

