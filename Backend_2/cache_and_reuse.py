
def save_expansion(clean_scrapped_content, chunk_id, topic, knowledge_expansion_collection):
    metadata = {
        "topic": topic#.lower().strip()
    }
    
    knowledge_expansion_collection.upsert(ids=chunk_id, documents=clean_scrapped_content, metadatas=metadata)#chunk_id here means the id of the chunk. It seems thats the id im using through out

    return "Saved to knowledge expansion database"


#Either we will send the entire chunk into the database as a query or we could find a way to extract the topic from the note and search by that
def find_cached_expansion(query, knowledge_expansion_collection):
    results = knowledge_expansion_collection.query(
                query_texts=[query],
                n_results=2
    )

    #return results

    if not results["ids"] or len(results["ids"][0]) == 0:
        return "None"

    distances = results["distances"][0][0]
    #if results["documents"] is None:
        #return "None"
    
    if distances > 0.45:
        knowledge_expansion = results["documents"][0][0]
        return "None"
    
    elif distances < 0.45:
        knowledge_expansion = results["documents"][0][0]
    else:
        return "None"
    
    return knowledge_expansion




def main():
    random_text = "If you want, I can give you: ✅ The function for saving this schema✅ The function for checking if topic exists✅ The function for retrieving cached expansions✅ The function for deciding whether to run the Knowledge Expansion LayerJust tell me:Give me the functions for this."
    topic = "Creating Functions" #This will be extracted from the scrapped content, when we scrape it, we'll seperate it from the rest of the content

    #Chunking this text
    from text_chunking import chunk_text_by_tokens
    all_chunks = chunk_text_by_tokens(random_text, max_tokens=250, overlap=50) #These are the chunks of text

    print(all_chunks)

    name = "a_test_database"

    from chroma_database import chroma_db
    knowledge_expansion_collection = chroma_db(name)


    for chunk in all_chunks:
        #Insert extracted text chunks into its own database 
        #knowledge_expansion_collection.upsert(ids=chunk["chunk_id"], documents=chunk["chunk_text"])#This will loop through all_chunk and adding the chunk to the database#This will loop through all_chunk and adding the chunk to the database

        ids = chunk["chunk_id"]
        chunk_text = chunk["chunk_text"]
        print(ids)
        save_the_expansion = save_expansion(chunk_text, chunk, ids, topic, knowledge_expansion_collection)
        #print(save_the_expansion)

    query = "I want to have The function for saving this schema and retrieving cached expansions"
    find_a_cached_expansion = find_cached_expansion(query, knowledge_expansion_collection)

    #print(find_a_cached_expansion)
    
#if __name__ == "__main__":
    #main()