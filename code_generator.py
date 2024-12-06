import webbrowser

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.generated_code = ""
        self.styles = ""  
        self.body_content = "" 

    def generate(self):
        # generate lower level language (html)
        self.traverse(self.ast)
        self.generated_code = f"""<!DOCTYPE html>
    <html>
    <head>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed
            }}
            th {{
                text-align: left;
                padding: 10px;
                border: 1px solid black;
            }}
            td {{
                padding: 8px;
                border: 1px solid black;     
            }}
            tr {{
                display: table-row;
            }}
            {self.styles}  
        </style>
    </head>
    <body>
        {self.body_content}
    </body>
    </html>
    """
        return self.generated_code


    def traverse(self, node):
        # process AST
        if node is None:
            return

        if node.node_type == "S":
            for child in node.children:
                self.traverse(child)
        elif node.node_type == "A":
            for child in node.children:
                if child.node_type == "WD":
                    # new table per day
                    self.body_content += f"<table><tr><th colspan='2'>{child.value}</th></tr>"
                elif child.node_type == "SCH":
                    self.process_schedule(child)
                elif child.node_type == "COM":
                    self.process_comment(child)
            self.body_content += "</table><br>"
            for child in node.children:
                if child.node_type == "A":
                    self.traverse(child)
        elif node.node_type == "B":
            # style 
            for child in node.children:
                if child.node_type == "ST":
                    style = child.children[0].value
                    value = child.children[2].value
                    if style == "heading_color":
                        self.styles += f"th {{ background-color: pink; }}" # replace rose-pink with pink bc wasnt rendering otherwise

    def process_schedule(self, node, last_end_time=None):
        # process a sch node and its children
        if node is None:
            return

        task = node.children[0].value
        start_time = node.children[2].value

        if start_time == "CONT":
            if last_end_time is not None:
                start_time = last_end_time
            else:
                start_time = "?"  
    
        if node.children[4].node_type == "Time":
            end_time = node.children[4].value
        else:
            end_time = "?"

        task_content = task
        task_content += self.extract_comments(node)
        self.body_content += f"<tr><td>{start_time}-{end_time}</td><td>{task_content}</td></tr>"

        last_end_time = end_time

        for child in node.children:
            if child.node_type == "SCH":
                self.process_schedule(child, last_end_time)

    def extract_comments(self, node):
        # make sure to get all comments 
        comment_content = ""
        for child in node.children:
            if child.node_type == "COM":
                comment = child.children[1].value
                comment_content += f"<br><span style='color: gray; font-size: smaller;'>{comment}</span>"

                comment_content += self.extract_comments(child)
        return comment_content

    def process_comment(self, node):
        # process comment node
        if node is None:
            return

        # get the text 
        comment = node.children[1].value
        self.body_content += f"<tr><td colspan='2' style='color: gray; font-size: smaller;'>{comment}</td></tr>"

        for child in node.children:
            if child.node_type == "COM":
                self.process_comment(child)

    def save_to_file(self, filename="output.html"):
        # save generated code to file (to be presented as html)
        try:
            with open(filename, "w") as file:
                file.write(self.generated_code)
            print(f"Generated code saved to {filename}")
        except Exception as e:
            print(f"Error saving to file: {str(e)}")

    def execute(self, filename="output.html"):
        # display output in browser 
        try:
            webbrowser.open(filename)
            print(f"Opened {filename} in web browser.")
        except Exception as e:
            print(f"Error opening file in browser: {str(e)}")

    def run_pipeline(self):
        # pipeline to output the generated code 
        try:
            print("Starting code generation...")
            self.generate()
            print("Code generation complete. Saving to file...")
            self.save_to_file()
            print("File saved. Executing...")
            self.execute()
        except Exception as e:
            print(f"Pipeline Error: {str(e)}")
