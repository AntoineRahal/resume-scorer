# Resume Scoring and Ranking

## *How can we automate the process of scoring and ranking resumes?*

![banner](./image/1554726063109.jpg)

## 1. Overview

The purpose of this project is to automate the tedious task of manual processing  of CVs by creating a tool that gives a score to a CV based on a given job description. To achieve this goal, the tool will be implemented using a natural language processing approach. A lexicon of skills is first built and the skills are grouped by job to help identify which skills are most unique to a job. Term frequency inverse document frequency (TF-IDF) is used to assign weights for skills. The scoring be done by extracting all the set of relevant skill from the job description and then the resume then mapping the document into a vector space in which each skill identified in the job description is a dimension. Finally, we can compute skill similarity between the documents by computing cosine similarity between the skills vectors for each document. Consequently, this tool boosts the recruitment process of candidates by identifying the resumes that are the most similar to a specific job description.

The web app can be found [here](https://antoinerahal-resume-scorer-main-rzzew6.streamlitapp.com).

## 2. Business Problem

Curriculum vitae (CVs), also known as resumes, continue to be a crucial standard document and a key decision element in selecting candidates and assessing their experience. Its primary function is to determine applicants' eligibility for a job position. However, corporate companies and recruitment agencies process an increasing number of CVs daily which constitutes a challenge for human recruiters. In fact, they need to spend long hours scrutinizing and analysing these documents by matching the candidates’ s technical and soft skills with that required by the job posts. In addition of being time consuming, the process may be subjective and partial since some recruiters do not follow professional standards in recruiting talent. The challenge emerges in finding the right candidate with the right skills in a short amount of time and without any type of prejudice or stereotyping.

## 3. Data

The data was scraped from [LinkedIn Career Explorer](https://linkedin.github.io/career-explorer/) which is tool that helps people uncover careers they could transition into and might not have considered, by mapping the skills they have to thousands of job titles. The Career Explorer tool leverages the vast amount of data contained in LinkedIn’s professional social media platform and help identify which skills are most vital to a specific job. It uses the aggregated profile information of LinkedIn's 706+ million members around the world.

The data was scraped using Selenium and Beautiful Soup which are Python libraries that support browser automation and HTML and XML documents parsing. The data consists of jobs and their respective skills and it was obtained by web scraping. The first step consisted of building a list of all the available cities available in the LinkedIn Career Explorer, then looping over the cities and then building a list of all the jobs in each city and looping over them to find the different jobs and their respective skills in different cities. For this project, Jobs and their respective skills from around 200 cities were scraped, resulting in around 2300 unique jobs and around 4000 unique skills.

The data was then stored in a MySQL relational database using many-to-many relationship between jobs and skills in addition to CSV format.

### 3.1 Creating a Dataframe of Skills Grouped by Job

A separate dataframe of skills grouped by job is created, this step would help identify which skills are most unique to a job and which skills are common across a wide range of jobs. The first column of the dataframe consist of the name of the job and the second includes a list of comma-separatedskills for a specific job, thus each row represents all the skills relevant to a specific job.

| Column Name | Description |
|-|-|
| job_name | The name of the job position |
| job_skills | A list of all the unique skills relevant to the job position |
