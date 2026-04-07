from langchain.messages import AIMessage


def test_calls_basic(iterations: int):
    from langchain_core.messages.content import ToolCall
    if iterations == 0:
        response = AIMessage(content="AAAAAAA", tool_calls=[
            ToolCall(
                name="AddClass",
                args={
                    "subject": "RandomSubject",
                    "type": "fhkb:Person"
                },
                id="0"
            ),
            ToolCall(
                name="AddTriple",
                args={
                    "subject": "RandomSubject2",
                    "relation": "fhkb:hasAncestor",
                    "object": "RandomObject"
                },
                id="1"
            ),
            ToolCall(
                name="ValidateShacl",
                args={},
                id="2"
            )
        ])
    elif iterations == 1:
        response = AIMessage(content="AAAAAAAAAA", tool_calls=[
            ToolCall(
                name="RemoveClass",
                args={
                    "subject": "RandomSubject",
                    "type": "fhkb:Person"
                },
                id="3"
            ),
            ToolCall(
                name="RemoveTriple",
                args={
                    "subject": "RandomSubject2",
                    "relation": "fhkb:hasAncestor",
                    "object": "RandomObject"
                },
                id="4"
            ),
            ToolCall(
                name="AddTriple",
                args={
                    "subject": "RandomSubject2",
                    "relation": "fhkb:hasPartner",
                    "object": "RandomObject"
                },
                id="5"
            )
        ])
    elif iterations == 2:
        response = AIMessage(content="AAAAAAAAA", tool_calls=[
            ToolCall(
                name="ValidateShacl",
                args={},
                id="6"
            )
        ])
    elif iterations == 3:
        response = AIMessage(content="AAAAAAAA", tool_calls=[
            ToolCall(
                name="Finish",
                args={},
                id="7"
            )
        ])
    elif iterations == 4:
        response = AIMessage(content="AAAAAA", tool_calls=[
            ToolCall(
                name="AddClass",
                args={
                    "subject": "RandomSubject2",
                    "type": "fhkb:Person"
                },
                id="8"
            ),
            ToolCall(
                name="AddClass",
                args={
                    "subject": "RandomObject",
                    "type": "fhkb:Woman"
                },
                id="9"
            )
        ])
    else:
        response=AIMessage(content="(((((((((((((((())))))))))))))))")
    
    return response