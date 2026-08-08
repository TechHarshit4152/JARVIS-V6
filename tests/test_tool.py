from jarvis_v6.tools.base import Tool

class TestTool(Tool):


    name = "test.tool"
    description = "A test tool"
    parameters={}

    def execute(self, **kwargs):
        return "Tool executed successfully."


tool = TestTool()

print(tool.name)
print(tool.description)
print(tool.parameters)
print(tool.execute())