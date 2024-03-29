from langchain.prompts import PromptTemplate


# template="""{dummy}Give me a single, specific topic to write an informative, engaging blog about.
# This blog topic must be relevant and appealing to many people so that many readers will want to read about it.
# The specific topic can be from a wide range of broader topics like physics, science, engineering, lifestyle, health, learning, teaching, history, technology, cryptocurrency, art, music, sport, business, economics, travel, entertainment, gaming, food, etc.
# Only give me the specific topic name after this prompt and nothing else. The topic is:"""
topic_prompt = PromptTemplate(
        input_variables=["dummy"],
        template="""{dummy}Give me a single, specific topic to write an informative, engaging gold related blog about.
This blog topic must be relevant and appealing to many people so that many readers will want to read about it.
The specific topic can be from a wide range of broader topics like the fundamental value of gold, Gold as a form of money, Gold's role as a safe haven, Gold mining and production, Gold's uses outside of jewelry and international reserves, The social and psychological aspects of gold,
Gold's future prospects, Gold standard vs. fiat currencies, Gold as a store of value, Gold's impact on the global economy, Gold jewellery demand and trends, Gold investment and portfolio management, Gold as a hedge against inflation, Gold bars and coins pricing and purchasing, Gold purity and quality standards, Gold mining and production, Gold trading and market analysis, Gold ETFs and mutual funds, Gold futures and options trading,
Gold reserves and central bank holdings etc.
The topic should not reflect the history, should reflect new ideas, trends, and news.
Only give me the specific topic name after this prompt and nothing else. The topic is:"""
    )

keyword_prompt = PromptTemplate(
        input_variables=["topic"],
        template="Give me a list of 5 keywords that for using in blog about {topic}",
    )

content_prompt = PromptTemplate(
    input_variables=["topic", "doc_1", "doc_2", "doc_3"],
    template="""Write a blog post about: {topic}. 
The blog post should have the following characteristics:
- The style and tone of the blog should be informative. You should write in the first person and use a friendly and engaging voice.
- The length of the blog post should be roughly 1300 words.
- The blog must contain these sections: introduction, body, and conclusion.
- The title should use h1 tag.
- Each section should have a clear and catchy heading that summarizes its main point.
- Use subheadings, bullet points, lists, quotes, or other elements to break up the text and make it easier to read.
- You should explain why the topic is relevant and important for the audience, what problem or challenge it addresses, how it can be solved or improved, what benefits or advantages it offers, and what action or step the reader should take next.
- Use relevant keywords strategically throughout the blog post to optimize it for search engines and attract more readers. You should also avoid keyword stuffing or using irrelevant or misleading keywords that do not match the content of the blog post.
- Use a catchy title, summary,  a hook sentence, a clear thesis statement, a compelling story or anecdote, a surprising fact or statistic, a relevant question or challenge, a strong conclusion.
- You should use these components to capture the attention of the reader and convey the main message and purpose of the blog
- The output format of the entire blog post must be in HTML format. All headings, bullet points, links, etc. must use proper HTML syntax
- The output article must include <body> HTML tag.
Please follow these instructions carefully and write a high-quality and original blog post about: {topic}.
Searching around the web, I've found this ADDITIONAL INFORMATION from distinct articles.
----------------
{doc_1}
----------------
{doc_2}
----------------
{doc_3}
----------------

Consider information from the previous ADDITIONAL INFORMATION.
Start immediately with the content of the blog post:"""
)
