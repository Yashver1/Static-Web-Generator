class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag 
        self.value = value
        self.children = children 
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        prop_string = " "
        for key,value in self.props.items():
            prop_string+=f"{key}=\"{value}\" " #space between props maintained
    
        return prop_string.rstrip()
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
            
    def __eq__(self,other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value does not exist")
        if self.tag == None:
            return self.value
            
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"

    def __eq__(self,other):
        if self.tag == other.tag and self.value==other.value and self.props==other.props:
            return True
        else:
            return False

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)

    def to_html(self):

        result = ""

        if not self.children: #handles [] and None both cases of children
            raise ValueError("children does not exist")

        if not self.tag:
            raise ValueError("tag does not exist")

        for node in self.children:
            result+=node.to_html()

        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag},{self.children},{self.props})"
            

    def __eq__(self,other):
        if self.tag == other.tag and self.children  == other.children and self.props == other.props:
            return True
        else:
            return False

    

