from langchain.messages import AIMessage


def test_calls_basic(iterations: int):
    from langchain_core.messages.content import ToolCall
    if iterations == 0:
        response = AIMessage(content="AAAAAAA", tool_calls=[
            ToolCall(
                name="AssignClass",
                args={
                    "source": "RandomSubject",
                    "type": "data:Person"
                },
                id="0"
            ),
            ToolCall(
                name="AddTriple",
                args={
                    "source": "RandomSubject2",
                    "relation": "data:hasAncestor",
                    "target": "RandomObject"
                },
                id="1"
            ),
            ToolCall(
                name="AddLiteral",
                args={
                    "source": "RandomSubject",
                    "relation": "data:hasBirthYear",
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
                    "source": "RandomSubject",
                    "type": "data:Person"
                },
                id="3"
            ),
            ToolCall(
                name="RemoveTriple",
                args={
                    "source": "RandomSubject2",
                    "relation": "data:hasAncestor",
                    "target": "RandomObject"
                },
                id="4"
            ),
            ToolCall(
                name="AddTriple",
                args={
                    "source": "RandomSubject2",
                    "relation": "data:hasPartner",
                    "target": "RandomObject"
                },
                id="5"
            ),
            ToolCall(
                name="RemoveLiteral",
                args={
                    "source": "RandomSubject",
                    "relation": "data:hasBirthYear",
                    "literal_value": "2026-01-01",
                    "literal_type": "xsd:date"
                },
                id="171"
            ),
            ToolCall(
                name="AddLiteral",
                args={
                    "source": "RandomSubject",
                    "relation": "data:hasBirthYear",
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
                    "source": "RandomSubject2",
                    "type": "data:Person"
                },
                id="8"
            ),
            ToolCall(
                name="AssignClass",
                args={
                    "source": "RandomObject",
                    "type": "data:Woman"
                },
                id="9"
            )
        ])
    else:
        response=AIMessage(content="(((((((((((((((())))))))))))))))")
    
    return response


def test_calls_basic1(iterations: int):
    from langchain_core.messages.content import ToolCall
    if iterations == 0:
        response = AIMessage(content="AAAAAAA", tool_calls=[
            ToolCall(
                name="AssignClass",
                args={
                    "source": "RandomSubject",
                    "type": ":Person"
                },
                id="9"
            ),
            ToolCall(
                name="AddTriple",
                args={
                    "source": "RandomSubject",
                    "relation": ":hasSister",
                    "target": "RandomObject"
                },
                id="0"
            ),
            ToolCall(
                name="AddTriple",
                args={
                    "source": "RandomSubject",
                    "relation": ":hasDaughter",
                    "target": "RandomObject"
                },
                id="1"
            ),
            ToolCall(
                name="AddLiteral",
                args={
                    "source": "RandomSubject",
                    "relation": ":hasBirthYear",
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
                name="RemoveTriple",
                args={
                    "source": "RandomSubject",
                    "relation": ":hasSister",
                    "target": "RandomObject"
                },
                id="50"
            ),
            ToolCall(
                name="Finish",
                args={},
                id="7"
            )
        ])
    elif iterations == 3:
        response = AIMessage(content="AAAAAA", tool_calls=[
            ToolCall(
                name="ValidateShacl",
                args={},
                id="2"
            )
        ])
    elif iterations == 4:
        response = AIMessage(content="AAAAAA", tool_calls=[
            ToolCall(
                name="Finish",
                args={},
                id="2"
            )
        ])
    else:
        response=AIMessage(content="(((((((((((((((())))))))))))))))")
    
    return response