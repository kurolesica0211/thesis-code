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
Total violations:4
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Elizabeth_II
    Path: hasMother
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: Elizabeth_II
    Path: hasMother
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [3]:
    Severity: Violation
    Focus node: Elizabeth_II
    Path: hasMother
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [4]:
    Severity: Violation
    Focus node: Elizabeth_II
    Path: hasMother
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Elizabeth_II has a \'hasMother\' relationship with George_VI, but the class of George_VI is \':Man\', which contradicts the requirement that the object of \'hasMother\' must be an instance of \':Woman\'.",\n      "instruction": "RemoveTriple(Elizabeth_II, hasMother, George_VI)"\n    },\n    {\n      "explanation": "The node Elizabeth_II has a \'hasMother\' relationship with George_VI, but the class of George_VI is \':Man\', which contradicts the requirement that the object of \'hasMother\' must be an instance of \':Woman\'.",\n      "instruction": "RemoveTriple(Elizabeth_II, hasMother, George_VI)"\n    },\n    {\n      "explanation": "The node Elizabeth_II has a \'hasMother\' relationship with George_VI, but the class of George_VI is \':Man\', which contradicts the requirement that the object of \'hasMother\' must be an instance of \':Woman\'.",\n      "instruction": "RemoveTriple(Elizabeth_II, hasMother, George_VI)"\n    },\n    {\n      "explanation": "The node Elizabeth_II has a \'hasMother\' relationship with George_VI, but the class of George_VI is \':Man\', which contradicts the requirement that the object of \'hasMother\' must be an instance of \':Woman\'.",\n      "instruction": "RemoveTriple(Elizabeth_II, hasMother, George_VI)"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHCrjb6tF16yDlxlreZhFVbNUhqgTUPZ2mAXRv8QMiXsigZsm9s+RstVC3h7Gm'}}]