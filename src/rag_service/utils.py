def format_docs(docs):
    return "\n\n".join(
        [
            f"""{d.page_content[:1200]} \n meta: \n {'\n'.join([f"{k}: {v}" for k, v in d.metadata.items()])}"""
            for d in docs
        ]
    )
