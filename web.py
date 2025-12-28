from collections import deque

class BrowserHistory:
    def __init__(self):
        self.back_stack = []    
        self.forward_stack = []
        self.closed_tabs = deque(maxlen=5)
        self.current_page = None

    def visit(self, page):
        if self.current_page:
            self.back_stack.append(self.current_page)
        self.current_page = page
        self.forward_stack.clear() 
        print(f"Visited: {page}")

    def back(self):
        if not self.back_stack:
            print("No pages in Back history.")
            return
        self.forward_stack.append(self.current_page)
        self.current_page = self.back_stack.pop()
        print(f"Back to: {self.current_page}")

    def forward(self):
        if not self.forward_stack:
            print("No pages in Forward history.")
            return
        self.back_stack.append(self.current_page)
        self.current_page = self.forward_stack.pop()
        print(f"Forward to: {self.current_page}")

    def close_tab(self):
        if self.current_page:
            self.closed_tabs.append(self.current_page)
            print(f"Closed tab: {self.current_page}")
            self.current_page = None
        else:
            print("No tab open to close.")

    def show_status(self):
        print("\n===== Browser Status =====")
        print(f"Current Page: {self.current_page}")
        print(f"Back Stack: {self.back_stack}")
        print(f"Forward Stack: {self.forward_stack}")
        print(f"Recently Closed Tabs: {list(self.closed_tabs)}")
        print("==========================\n")


browser = BrowserHistory()

browser.visit("Google")
browser.visit("YouTube")
browser.visit("INSTA")

browser.close_tab()

#browser.visit("FAC")

browser.show_status()
browser.visit("wiki")

browser.close_tab()

#browser.visit("FAC")

browser.show_status()