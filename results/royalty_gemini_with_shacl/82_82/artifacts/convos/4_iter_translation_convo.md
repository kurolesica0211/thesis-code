================================ System Message ================================

### Role
You are a SHACL (Shapes Constraint Language) Interpretation Expert. Your task is to translate technical validation reports into human-readable explanations and specific instructions for a Knowledge Graph editing agent.

### Context
The editing agent is building a Knowledge Graph and has access to the following tools:
- `AssignClass`: Assigns a class (rdf:type) to a node.
- `AddTriple`: Adds a relationship between two nodes.
- `UnassignClass`: Removes a class assignment.
- `RemoveTriple`: Deletes a relationship.
- `AddLiteral`: Adds a relationship between a node and a raw datapoint (literal)
- `RemoveLiteral`: Removes a relationship.

### Your Task
For every SHACL violation provided, you must generate a structured response containing:
1. **Explanation**: A clear, non-technical description of what is wrong. Identify the specific node (focusNode), the property (path) involved, and the nature of the error (e.g., a missing mandatory property, an invalid class, or too many instances of a relation).
2. **Instruction**: A direct command telling the agent exactly which tool to use and what data to provide to fix the violation.

### Guidelines
- Be specific. Mention the nodes and properties with the namespace prefixes.
- If a node is missing a class, instruct the agent to use `AssignClass`.
- If a mandatory relation is missing, instruct the agent to use `AddTriple`.
- Keep the tone professional, concise, and helpful.

================================ Human Message =================================

The SHACL validation process has identified the following violations in the current data graph:

---
### Violations:
VALIDATION RESULTS
Total violations:2
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Beatrice_Elizabeth_Mapelli_Mozzi
    Path: None
    Value: Beatrice_Elizabeth_Mapelli_Mozzi
    Constraint: ClassConstraintComponent
    Source shape:
      esh:DomainConjunctionShape_isMotherOf a sh:NodeShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:message "Any subject of isMotherOf must be all of: Ancestor, Woman." ;
          sh:targetSubjectsOf :isMotherOf .
    SHACL message: Any subject of isMotherOf must be all of: Ancestor, Woman.
    Classes assigned to the focus node: []
    Definitions of the classes assigned to the focus node:

    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:



  Violation [2]:
    Severity: Violation
    Focus node: Beatrice_Elizabeth_Mapelli_Mozzi
    Path: None
    Value: Beatrice_Elizabeth_Mapelli_Mozzi
    Constraint: ClassConstraintComponent
    Source shape:
      esh:DomainConjunctionShape_isMotherOf a sh:NodeShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:message "Any subject of isMotherOf must be all of: Ancestor, Woman." ;
          sh:targetSubjectsOf :isMotherOf .
    SHACL message: Any subject of isMotherOf must be all of: Ancestor, Woman.
    Classes assigned to the focus node: []
    Definitions of the classes assigned to the focus node:

    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Beatrice_Elizabeth_Mapelli_Mozzi is missing the mandatory class assignment for \':Ancestor\', which is required because she is the subject of an \'isMotherOf\' relationship.",\n      "instruction": "AssignClass(node=\'Beatrice_Elizabeth_Mapelli_Mozzi\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Beatrice_Elizabeth_Mapelli_Mozzi is missing the mandatory class assignment for \':Woman\', which is required because she is the subject of an \'isMotherOf\' relationship.",\n      "instruction": "AssignClass(node=\'Beatrice_Elizabeth_Mapelli_Mozzi\', class=\':Woman\')"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHG931/zMArTRbd2doaDEcyBHOT8l/ZeUMCjK3LPN4BDcPPnkSV8NC4BdDAjTl'}}]