import streamlit

class Pages:
    def __init__(self, navigation_name: str = 'navigation', st: streamlit = streamlit) -> None:
        self.app = dict()
        self.navigation_name = navigation_name
        self.st = st
        self.func_parmeter = dict()
    
    def add_app(self, name: str, func: any) -> None:
        self.app[name] = func

            
    def run(self):
        self.st.sidebar.markdown("""
        <h2 class='sub-title'>Steps</h2>
        """, unsafe_allow_html=True)
        select_app = self.st.sidebar.selectbox(self.navigation_name, self.app.keys())
        return self.app[select_app]()

        