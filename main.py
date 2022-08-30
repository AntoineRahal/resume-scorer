## Libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from io import StringIO
import PyPDF2
import docx
from nltk.tokenize import regexp_tokenize
import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy
import json
import jsonlines
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import plotly.express as px
import re
import io
import pdfminer.high_level


## Load pre-trained model
nlp = spacy.load("en_core_web_sm")

# Add the Entity Ruler to the spacy pipeline
with jsonlines.open("my_patterns.jsonl") as f:
    created_entities = [line['label'].upper() for line in f.iter()]

ruler = nlp.add_pipe("entity_ruler", after='parser')
ruler.from_disk("my_patterns.jsonl")


## Functions

# read PDF file
def extract_text_from_pdf(file):
    '''Opens and reads in a PDF file'''
    
    text = pdfminer.high_level.extract_text(file)
    str_list = text.split()
    str_list = str_list[:]
    string = ' '.join(str_list)
    
    return string


# read word doc file
def extract_text_from_word(file):
    '''Opens en reads in a .doc or .docx file'''

    doc = docx.Document(file)      
    text = [para.text for para in doc.paragraphs]

    return ' '.join(text)


# custom tokenizer for skills
def tokenize(text):
    '''Custom tokenizer'''

    words = regexp_tokenize(text, pattern=r",(?=[\S])", gaps=True)

    return words


def extract_skills(text):
    '''Extract skills from text'''
    
    doc = nlp(text)
    skills = set([ent.label_[6:] for ent in doc.ents if 'skill' in ent.label_.lower()])
    
    return ",".join(list(skills))


## Load the saved tfidf vectorizer
with open("tfidf.pkl", 'rb') as file:
    tfidf_vectorizer = pickle.load(file)




## Page Configuration
st.set_page_config(page_title="Resume Scorer",
                   page_icon=":page_facing_up:",
                   layout="wide")


st.title('Resume Scorer')
img = Image.open('1554726063109.jpg')
st.image(img)
st.markdown("""

    <div style="text-align: justify;">
    This project aims to score a resume based on a given job description. Corporate companies process an increasing number of CVs daily which constitutes a challenge for human recruiters. The purpose of this project is to make the task of processing CVs faster by creating a tool that compares the skills in the CVs and the job description and give a score accordingly.

    <br></br>

    """,unsafe_allow_html = True)



resume_file_list = st.file_uploader("Upload your resume", type=["pdf","docx"], accept_multiple_files=True)
job_des_file = st.file_uploader("Upload the job description", type=["pdf","docx"], accept_multiple_files=False)


df = pd.DataFrame(columns = ['name', 'text'])


if job_des_file is not None:
	if job_des_file.type in 'application/pdf':
		jd_text = extract_text_from_pdf(job_des_file)
		row = {'name':'Job Description', 'text':jd_text}
		df = df.append(row, ignore_index=True)

	if job_des_file.type in 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
		jd_text = extract_text_from_word(job_des_file)
		row = {'name':'Job Description', 'text':jd_text}
		df = df.append(row, ignore_index=True)



if resume_file_list != []:
	for resume_file in resume_file_list:
		if resume_file.type in 'application/pdf':
			cv_text = extract_text_from_pdf(resume_file)
			row = {'name':resume_file.name, 'text':cv_text}
			df = df.append(row, ignore_index=True)

		if resume_file.type in 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
			cv_text = extract_text_from_word(resume_file)
			row = {'name':resume_file.name, 'text':cv_text}
			df = df.append(row, ignore_index=True)

#st.write(df)

if "button_clicked" not in st.session_state:
	st.session_state["button_clicked"] = False


def callback():
	# Button was clicked
	st.session_state["button_clicked"] = True

def callback2():
	# Button was clicked
	st.session_state["button_clicked"] = False


if (
	st.button('Get Scores', on_click=callback)
	or st.session_state["button_clicked"]
	):

	try:


		doc_jd = nlp(df[df['name']=='Job Description']['text'][0])
		options = {"ents": created_entities}
		ent_html = displacy.render(doc_jd, style='ent', options=options, jupyter=False)
		st.subheader('Skills identified in the job description')
		visualization = st.markdown(ent_html, unsafe_allow_html=True)
		st.markdown("""<br></br>""",unsafe_allow_html = True)








		st.subheader('Enter skills that didn\'t match:')
		new_skill = st.text_input('Please enter the pattern of skill(s) as written in the text (comma separated)', on_change=callback)
		feature_array = tfidf_vectorizer.get_feature_names_out()
		xxxx = st.multiselect('Select the skill(s) that match the previous pattern', options=feature_array, on_change=callback)
		if new_skill:
			if xxxx:
				new_skill = new_skill.split(',')
				for i in range(len(xxxx)):
					split_skill = new_skill[i].strip()
					split_skill = split_skill.split()
					pattern=[] 
					for N in range(len(split_skill)):
						pattern.append({"LOWER":f"{split_skill[N].lower()}"})
					skill = " ".join(split_skill)    
					x = {"label":f"SKILL|{xxxx[i]}","pattern":pattern} 
					ruler.add_patterns([x])



	#	df['skills'] = df['text'].apply(extract_skills)
	#	st.write(df)


		doc_jd = nlp(df[df['name']=='Job Description']['text'][0])
		options = {"ents": created_entities}
		ent_html = displacy.render(doc_jd, style='ent', options=options, jupyter=False)
#		st.subheader('Skills identified in the job description')
		visualization.markdown(ent_html, unsafe_allow_html=True)
#		st.markdown("""<br></br>""",unsafe_allow_html = True)

		job_description_skills = set([ent.label_[6:] for ent in doc_jd.ents if 'skill' in ent.label_.lower()])
		
		if new_skill:
			if xxxx:
				for i in range(len(xxxx)):
					job_description_skills.add(xxxx[i])


		st.subheader('Remove the skills that don\'t match properly')			
		selected_skills = st.multiselect('Remove the skills that are not matched properly in the job description:', options=job_description_skills, default=job_description_skills, on_change=callback)


#		st.subheader('Skills identified in the job description')
#		st.markdown(ent_html, unsafe_allow_html=True)
#		st.markdown("""<br></br>""",unsafe_allow_html = True)


		def extract_skills(text):
			doc = nlp(text)
			skills = set([ent.label_[6:] for ent in doc.ents if 'skill' in ent.label_.lower()])

			return ",".join(list(skills))


		df['skills'] = df['text'].apply(extract_skills)



		st.write(df['skills'])






		if st.button('Reset the page', on_click=callback2):
			st.write('Reset')

		tfidf_matrix = tfidf_vectorizer.transform(df['skills'])
		feature_array = tfidf_vectorizer.get_feature_names_out()
		dense = tfidf_matrix.toarray()
		df_tfidf = pd.DataFrame(data=dense, columns=feature_array)
		df_tfidf = df_tfidf[selected_skills]
		cos_sim = cosine_similarity(df_tfidf)[0][1:]

		similarity_df =  pd.DataFrame(cos_sim, columns=['Similarity'])
		similarity_df['Doc Name'] = np.array(df['name'][1:])
		similarity_df.sort_values(by='Similarity', axis=0, ascending=False, inplace=True)
		similarity_df.reset_index(drop=True, inplace=True)
		st.subheader('Weight Table')
		df_tfidf2 = df_tfidf.set_index(np.array(df['name']))
		st.write(df_tfidf2)
		st.subheader('Most Similar documents to the job description')
		st.write(similarity_df)

		fig = px.bar(similarity_df, x='Similarity', y='Doc Name', 
	             width=1500, 
	             height=1000,
	           	 labels={"Doc Name": ""},
	             title="Similarity of CVs to the job description",
	            )

		fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
		fig.update_yaxes(categoryorder="total ascending")
		#fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,width=0.2)
		st.write(fig)

	except:
		st.write('Please upload files')