from langchain.messages import AIMessage


def test_calls_basic(iterations: int):
    from langchain_core.messages.content import ToolCall
    if iterations == 0:
        response = AIMessage(content="AAAAAAA", tool_calls=[
            ToolCall(
                name="AssignClass",
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
                name="AddLiteral",
                args={
                    "subject": "RandomSubject",
                    "relation": "fhkb:hasBirthYear",
                    "literal_value": "2026-01-01",
                    "literal_type": "xsd:date"
                },
                id="170"
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
                name="UnassignClass",
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
            ),
            ToolCall(
                name="RemoveLiteral",
                args={
                    "subject": "RandomSubject",
                    "relation": "fhkb:hasBirthYear",
                    "literal_value": "2026-01-01",
                    "literal_type": "xsd:date"
                },
                id="171"
            ),
            ToolCall(
                name="AddLiteral",
                args={
                    "subject": "RandomSubject",
                    "relation": "fhkb:hasBirthYear",
                    "literal_value": "aaa",
                    "literal_type": "xsd:integer"
                },
                id="187"
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
                name="AssignClass",
                args={
                    "subject": "RandomSubject2",
                    "type": "fhkb:Person"
                },
                id="8"
            ),
            ToolCall(
                name="AssignClass",
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