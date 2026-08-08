from jarvis_v6.tools.results import ToolResult

success = ToolResult(
    success=True,
    output="Tool executed successfully."
)

failure = ToolResult(
    success=False,
    error="Something went wrong."
)

with_metadata = ToolResult(
    success=True,
    output="Done.",
    metadata={"tool":"test.tool"}
)

print(success)
print(failure)
print(with_metadata)

assert success.success is True
assert success.output == "Tool executed successfully."

assert failure.success is False
assert failure.error == "Something went wrong."

assert with_metadata.metadata["tool"] == "test.tool"