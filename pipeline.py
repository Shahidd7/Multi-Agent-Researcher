from agents import build_search_agent,build_reader_agent,writer_chain,critic_chain

def run_research_pipeline(topic: str)-> dict:
    state = {}

    print("\n")
    #search agent 
    print("step 1 - search agent is working ...")

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
        (
            "user",
            f"""
            Research this topic thoroughly:
            {topic}
            Use the web_search tool to find external evidence.
            Preserve the titles, URLs, and relevant search results.
            """
        )
    ]
})

    state['search_results'] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])

    # Step 2: Reader agent

    print("\n")
    print("step 2 - Reader agent is scraping top resources ...")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
    "messages": [
    (
        "user",
        f"""
        Based on the following search results about '{topic}',
        select the most relevant URL and scrape it for deeper content
        Search Results:                        
        {state['search_results']}
        """
        )
                ]
    })
    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nScraped content:\n", state["scraped_content"])

    #step 3 - writer chain 

    combined_research = (
    f"SEARCH RESULTS:\n{state['search_results']}\n\n"
    f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": combined_research
    })
    print("\n Final Report\n",state['report'])

    # Step 4: Critic report
    print("\n")

    state['feedback'] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip()

    if topic:
        run_research_pipeline(topic)
    else:
        print("Please enter a research topic.")
