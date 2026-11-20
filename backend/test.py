# def test_init_hf_model():
#     chat=init_hf_model("mistralai/Mistral-7B-Instruct-v0.3")
#     messages = [
#         ("system", "You are a helpful assistant."),
#         ("human", "I love programming."),
#     ]
#     res = chat.invoke(messages)
#     print(type(res))
#     for chunk in chat.stream(messages):
#         print(chunk)
        
# def test_pdf_chat():
#     while True:
#         query = input("\n❓ Enter your question (type 'exit' to quit): ")
#         if query.strip().lower() == "exit":
#             print("👋 Goodbye!")
#             break

#         answer, sources = get_response(query)
        
#         print("\n📌 Answer:", answer)
#         print("\n📚 Source Documents:")
        
#         for i, doc in enumerate(sources, start=1):
#             print(f"\n--- Document {i} ---")
#             print(f"Source: {doc.metadata.get('source', 'Unknown')}")
#             print(doc.page_content)
#         print("\n")