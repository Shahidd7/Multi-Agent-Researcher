from dotenv import load_dotenv
from tools import web_search, scrape_url
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a professional web research agent.

        Your ONLY job is to search the web and gather external information.

        Rules:
        1. ALWAYS use the web_search tool.
        2. NEVER answer from your own knowledge.
        3. Search for recent and reliable sources.
        4. Return a maximum of 5 relevant sources.
        5. For each source include:
        - Title
        - URL
        - 1-2 sentence summary
        6. Keep your total response below 500 words.
        7. Do not write a long report.
        """
    )


def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
        You are a research reading agent.

        Your job is to read external web pages.

        Rules:
        1. ALWAYS use the scrape_url tool.
        2. Read the URL provided by the search agent.
        3. Extract only the most important factual information.
        4. Focus on:
        - important facts
        - numbers
        - dates
        - technical details
        - relevant claims
        5. Clearly identify the source URL.
        6. Do not repeat unnecessary information.
        7. Keep your response below 700 words.
        8. Do not write a final report.
        """
    )


writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are an expert research writer.

        Write a concise, factual research report.

        Rules:
        1. Use only the supplied research.
        2. Do not invent facts or sources.
        3. Keep the final report between 800 and 1000 words.
        4. Prioritize the most important findings.
        5. Avoid unnecessary tables.
        6. Include source URLs.
        7. Clearly distinguish facts from analysis.
        """),
    ("human", """Write a research report on:

    Topic: {topic}

    Research Gathered:
    {research}

    Structure:

    ## Introduction

    ## Key Findings

    ## Conclusion

    ## Sources

    Requirements:
    - Maximum 1000 words.
    - Minimum 500 words.
    - Focus only on the most important findings.
    - Use the supplied URLs as sources.
    - Do not repeat information.
    - Do not add unsupported claims.
    """),
])

writer_chain = writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are a sharp and constructive research critic.

        Be concise and specific.
        Keep your response below 250 words.
        """),
    ("human", """Review the report below.

        Report:
        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ...

        Keep the entire response below 250 words.
        """),
])

critic_chain = critic_prompt | llm | StrOutputParser()
