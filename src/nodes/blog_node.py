from langchain_classic.schema import HumanMessage
from src.states.blogstate import BlogState,Blog


class BlogNode:
    """
    A class to Represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        Create the title for the blog
        """
        if "topic" in state and state['topic']:
            prompt = """ 
                    You are an expert blog content writer. Use Markdown formatting. Generate a
                    blog title for the {topic}. This title should be creative and SEO Friendly.  
                    """
            
            system_message = prompt.format(topic = state['topic'])
            response =self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}
        
    def content_generation(self, state:BlogState):
        """
        Generate the detailed content for the blog
        """

        if "topic" in state and state['topic'] and "blog" in state and state['blog'] and "title" in state['blog'] and state['blog']['title']:
            system_prompt = """ 
                    You are an expert blog content writer. Use Markdown formatting. Generate a
                    detailed blog content for the {topic}. This content should be creative, engaging and SEO Friendly.  
                    """
            
            system_message = system_prompt.format(topic = state['topic'])
            response =self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
    def translation(self, state: BlogState):
        """
        Translate title and blog content to target language
        """

        translation_prompt = f"""
        Translate the following TITLE and BLOG CONTENT into {state['current_language']}.

        Maintain formatting and tone.

        TITLE:
        {state['blog']['title']}

        CONTENT:
        {state['blog']['content']}
        """

        message = [
            HumanMessage(content=translation_prompt)
        ]

        response = self.llm.invoke(message)

        # ---- SIMPLE SPLIT METHOD ----
        translated_text = response.content

        return {
            "blog": {
                "title": translated_text.split("CONTENT:")[0].replace("TITLE:", "").strip(),
                "content": translated_text.split("CONTENT:")[-1].strip()
            },
            "current_language": state["current_language"]
        }
    def route(self, state:BlogState):
        """
        Route the content to the respective translation node based on the language specified.
        """
        return state['current_language']
    
    def route_decision(self, state:BlogState):
        # """
        # Decide the route based on the language specified.
        # """
        # if state['current_language']=="hindi":
        #     return "hindi"
        # elif state['current_language']=="french":
        #     return "french"
        
        # else:
        #     return state
        return state['current_language']

        