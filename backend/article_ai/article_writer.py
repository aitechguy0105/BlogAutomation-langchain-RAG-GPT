import os
import logging
from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from .prompt_templates import content_prompt, topic_prompt
from langchain.prompts import PromptTemplate
from bs4 import BeautifulSoup
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI
import newspaper
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import openai
# for image
from datetime import datetime
import uuid
import requests
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_blog_chain():
    logging.info("Loading LLM config")
    # set up some parameters of the LLM
    # content_llm_kwargs = {
    #     "temperature": 0.7,
    #     "model": "gemini-pro",
    #     "max_output_tokens": 2048 # ~ 1500 words (max for gemini-pro)
    # }
    #
    # topic_llm_kwargs = {
    #     "temperature": 0.9,
    #     "model": "gemini-pro",
    #     "max_output_tokens": 50 # ~ 38words
    # }

    # create LLMs with kwargs specified above
    # content_llm = GoogleGenerativeAI(**content_llm_kwargs)
    # topic_llm = GoogleGenerativeAI(**topic_llm_kwargs)
    content_llm_kwargs = {
        "temperature": 0.7,
        "model_name": "gpt-3.5-turbo",
        "max_tokens": 1500  # ~ 1125 words
    }

    brief_llm_kwargs = {
        "temperature": 0.7,
        "model_name": "gpt-3.5-turbo",
        "max_tokens": 50  # ~ 38words
    }
    content_llm = OpenAI(**content_llm_kwargs)
    brief_llm = OpenAI(**brief_llm_kwargs)

    # chain it all together
    topic_chain = LLMChain(llm=brief_llm, prompt=topic_prompt)
    content_chain = LLMChain(llm=content_llm, prompt=content_prompt)

    chain = SimpleSequentialChain(
        chains=[
            topic_chain,
            content_chain
        ],
        verbose=True
    )

    return chain
class ArticleWriter():
    def __init__(self):

        print(os.environ.get('OPENAI_API_KEY'))
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    def get_image(self, topic):

        n = 1
        size = "512x512"

        response = openai.Image.create(
            prompt=topic,
            n=n,
            size=size
        )

        images = response["data"]
        
    #     headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    # }
        for image in images:
            url = image["url"]
            response = requests.get(url)
            response.raise_for_status()
            current_date_time = datetime.now()
            formatted_date_time = current_date_time.strftime("%Y%m%d%H%M%S")

            # Generate a unique identifier
            unique_id = str(uuid.uuid4())

            # Concatenate the date/time and unique identifier
            unique_string = formatted_date_time + "_" + unique_id
            with open(f"/home/vegaventures2/react-flask-app/blog_api/src/static/dist/images/{unique_string}.jpg", "wb") as f:
                f.write(response.content)
            return unique_string
            print('file save on local com')

    def get_query(self, topic):
        template = """You are an exceptional copywriter and content creator.

        You're reading an article with the following topic:
        ----------------
        {topic}
        ----------------

        What are some simple and high-level Google queries that you'd do to search for info to write article?
        Write 3 queries as a bullet point list, prepending each line with -.
        """

        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=template,
                input_variables=["topic"],
            )
        )

        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
        chat = ChatOpenAI(temperature=0.9)
        chain = LLMChain(llm=chat, prompt=chat_prompt_template)
        response = chain.run({

            "topic": topic
        })
        queries = [line[2:] for line in response.split("\n")]
        return queries

    def get_similar_content(self, queries, topic):
        search = GoogleSearchAPIWrapper()
        TOP_N_RESULTS = 5

        def top_n_results(query):
            return search.results(query, TOP_N_RESULTS)

        tool = Tool(
            name="Google Search",
            description="Search Google for recent results.",
            func=top_n_results
        )
        all_results = []

        for query in queries:
            results = tool.run(query)
            all_results += results

            if "title" in results[0]:  # Sample
                print(results[0]["title"])
                print(results[0]["link"])
                print(results[0]["snippet"])
                print("-" * 50)
        pages_content = []

        for result in all_results:
            try:
                article = newspaper.Article(result["link"])
                article.download()
                article.parse()
                if len(article.text) > 0:
                    pages_content.append({"url": result["link"], "text": article.text})
            except:
                continue

        print("Number of pages: ", len(pages_content))
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=100)

        docs = []
        for d in pages_content:
            chunks = text_splitter.split_text(d["text"])
            for chunk in chunks:
                new_doc = Document(page_content=chunk, metadata={"source": d["url"]})
                docs.append(new_doc)

        print("Number of chunks: ", len(docs))
        
        if len(docs) == 0:
            return None
        
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

        docs_embeddings = embeddings.embed_documents([doc.page_content for doc in docs])

        query_embedding = embeddings.embed_query(topic)

        def get_top_k_indices(list_of_doc_vectors, query_vector, top_k):
            # convert the lists of vectors to numpy arrays
            list_of_doc_vectors = np.array(list_of_doc_vectors)
            query_vector = np.array(query_vector)

            # compute cosine similarities
            similarities = cosine_similarity(query_vector.reshape(1, -1), list_of_doc_vectors).flatten()

            # sort the vectors based on cosine similarity
            sorted_indices = np.argsort(similarities)[::-1]

            # retrieve the top K indices from the sorted list
            top_k_indices = sorted_indices[:top_k]

            return top_k_indices

        top_k = 3
        best_indexes = get_top_k_indices(docs_embeddings, query_embedding, top_k)
        best_k_documents = [doc for i, doc in enumerate(docs) if i in best_indexes]
        return best_k_documents
    def create_article_openai(self, topic, debug=False):
        logging.info("Parsing CLI args")


        manual_topic_prompt = PromptTemplate(input_variables=["topic"], template="""Give me a single, specific topic to write an informative, engaging gold related blog about.
    This blog topic must be relevant and appealing to many people so that many readers will want to read about it.
   The specific topic can be from a wide range of broader topics like {topic}.
   The topic should not reflect the history, should reflect new ideas, trends, and news.
    Only give me the specific topic name after this prompt and nothing else. The topic is:""")
    
        summary_prompt = PromptTemplate(input_variables=["article"], template="""
        Given the article: {article}, I want you to write a short summary of the article in 20~30words. The answer should only include summary.
        Summary:
        """)
        

        logging.info("Loading LLM config")

        content_llm_kwargs = {
            "temperature": 0.7,
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 1500  # ~ 1125 words
        }

        brief_llm_kwargs = {
            "temperature": 0.7,
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 50  # ~ 38words
        }
        summary_llm_kwargs = {
            "temperature": 0.85,
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 50
        }

        content_llm = OpenAI(**content_llm_kwargs)
        brief_llm = OpenAI(**brief_llm_kwargs)
        summary_llm = OpenAI(**summary_llm_kwargs)
        
        # chain it all together
        if topic == "":
            topic_chain = LLMChain(llm=brief_llm, prompt=topic_prompt)
            print('auto topic')
        else:
            topic_chain = LLMChain(llm=brief_llm, prompt=manual_topic_prompt)
            print('manual topic')

        content_chain = LLMChain(llm=content_llm, prompt=content_prompt)
        summary_chain = LLMChain(llm = summary_llm, prompt=summary_prompt)
        if topic == "":
            topic = topic_chain.run("")
        else:
            topic = topic_chain.run(topic)

        queries = self.get_query(topic)
        docs = self.get_similar_content(queries, topic)
        print("Generating topic and blog (can take some time)...")
        
        if docs == None:
            blog_text = content_chain.run({"topic": topic, "doc_1": "", "doc_2": "", "doc_3": ""})
        elif len(docs) == 1:
            blog_text = content_chain.run({"topic": topic, "doc_1": docs[0].page_content, "doc_2": "", "doc_3": ""})
        elif len(docs) == 2:
            blog_text = content_chain.run({"topic": topic, "doc_1": docs[0].page_content, "doc_2": docs[1].page_content, "doc_3": ""})
        else: 
            blog_text = content_chain.run({"topic": topic, "doc_1": docs[0].page_content, "doc_2": docs[1].page_content, "doc_3": docs[2].page_content})
  
    


        if debug:
            return blog_text
        soup = BeautifulSoup(blog_text,'html.parser')
        article = str(soup.find('body'))
        if article == None:
            print('article none error')
            return None, None, None, None

        summary = summary_chain.run({"article": article})
        print('sumary:', summary)
        # paragraphs = soup.find_all('p')
        # if len(paragraphs) > 1:
        #     summary = paragraphs[0].get_text()
        #     print(summary)
        # else:
        #     print("There is no second paragraph in the webpage")

        
        title = soup.find('h1').get_text()
        
        print("image generating....")
        img_url = self.get_image(topic)
        img_tag = soup.new_tag('img', alt=topic, height='500', src=f"/images/{img_url}.jpg", width='500')
        img_url = f"/images/{img_url}.jpg"
# Insert the img tag after the h1 tag
        soup.h1.insert_after(img_tag)
        # print(str(soup))
        article = str(soup.find('body'))
        article = article.replace("<body>", "").replace("</body>", "")
        
        return title, summary, article, img_url


if __name__ == "__main__":

    load_dotenv('../.env')
    article_writer  =  ArticleWriter()
    title, summary, article = article_writer.create_article_openai("Gold Investment")
    print(article)
    # logging.info("Parsing CLI args")
    # parser = argparse.ArgumentParser(description="A create a blog post as a Markdown file with ecrivai")
    # parser.add_argument("--out-dir", type=str, default="./content", help="The path to the output directory")
    # args = parser.parse_args()
    #
    # chain = get_blog_chain()
    # logging.info("Generating topic and blog (can take some time)...")
    # blog_text = chain.run("")
    # logging.info("Blog content finished")
    #
    # out_dir = args.out_dir
    # logging.info(f"Writing blog to Markdown file at: {out_dir}")
    # md_file_name = to_markdown(blog_text, out_dir=out_dir)
    # logging.info(f"Formatting file header for Hugo")
    # blof_file_path = os.path.join(out_dir, md_file_name)
    # md2hugo(blof_file_path, blof_file_path)
    # logging.info(f"Done")

