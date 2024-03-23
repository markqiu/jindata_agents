from embedchain.store.assistants import AIAssistant

assistant = AIAssistant(
    name="My Assistant",
    data_sources=[{"source": "https://www.youtube.com/watch?v=U9mJuUkhUzk"}],
)

# Load an assistant and create a new thread
assistant = AIAssistant(assistant_id="asst_xxx")

# Load a specific thread for an assistant
assistant = AIAssistant(assistant_id="asst_xxx", thread_id="thread_xxx")

# assistant.add("/path/to/file.pdf")
assistant.add("https://www.youtube.com/watch?v=U9mJuUkhUzk")
assistant.add("https://openai.com/blog/new-models-and-developer-products-announced-at-devday")

print(assistant.chat("你是openai 公司开发的吗?"))
# Response: 'Every attendee of OpenAI DevDay 2023 was offered $500 in OpenAI credits.'
