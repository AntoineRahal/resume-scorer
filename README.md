# Resume Scoring and Ranking

## *How can we automate the process of scoring and ranking resumes?*

![banner](./image/1554726063109.jpg)

## Overview

The purpose of this project is to automate the tedious task of manual processing  of CVs by creating a tool that gives a score to a CV based on a given job description. To achieve this goal, the tool will be implemented using a natural language processing approach. A lexicon of skills is first built and the skills are grouped by job to help identify which skills are most unique to a job. Term frequency inverse document frequency (TF-IDF) is used to assign weights for skills. The scoring be done by extracting all the set of relevant skill from the job description and then the resume then mapping the document into a vector space in which each skill identified in the job description is a dimension. Finally, we can compute skill similarity between the documents by computing cosine similarity between the skills vectors for each document. Consequently, this tool boosts the recruitment process of candidates by identifying the resumes that are the most similar to a specific job description.

The web app can be found [here](https://antoinerahal-resume-scorer-main-rzzew6.streamlitapp.com).

## Business Problem

Curriculum vitae (CVs), also known as resumes, continue to be a crucial standard document and a key decision element in selecting candidates and assessing their experience. Its primary function is to determine applicants' eligibility for a job position. However, corporate companies and recruitment agencies process an increasing number of CVs daily which constitutes a challenge for human recruiters. In fact, they need to spend long hours scrutinizing and analysing these documents by matching the candidates’ s technical and soft skills with that required by the job posts. In addition of being time consuming, the process may be subjective and partial since some recruiters do not follow professional standards in recruiting talent. The challenge emerges in finding the right candidate with the right skills in a short amount of time and without any type of prejudice or stereotyping.

