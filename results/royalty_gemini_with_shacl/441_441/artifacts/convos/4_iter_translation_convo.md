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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [3]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [4]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Woman', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node \'Charles_Hepburn-Stuart-Forbes-Trefusis_20th\' has a \'hasFather\' relationship to \'Harriet_Williamina_Hepburn-Forbes\', but the target node is classified as a \':Woman\', while the property requires a \':Man\' or \':Ancestor\'.",\n      "instruction": "Use RemoveTriple to delete the relationship between \'Charles_Hepburn-Stuart-Forbes-Trefusis_20th\' and \'Harriet_Williamina_Hepburn-Forbes\' using the property \':hasFather\'."\n    },\n    {\n      "explanation": "The node \'Charles_Hepburn-Stuart-Forbes-Trefusis_20th\' has a \'hasFather\' relationship to \'Harriet_Williamina_Hepburn-Forbes\', which is incorrectly typed as a \':Woman\' in the context of the \'hasFather\' property.",\n      "instruction": "Use UnassignClass to remove the \':Woman\' class from \'Harriet_Williamina_Hepburn-Forbes\' if it is factually incorrect, or verify the relationship."\n    },\n    {\n      "explanation": "The property \'hasFather\' is restricted to values that are instances of \':Man\' or \':Ancestor\'. The current value \'Harriet_Williamina_Hepburn-Forbes\' violates this constraint.",\n      "instruction": "Use AddTriple to link \'Charles_Hepburn-Stuart-Forbes-Trefusis_20th\' to the correct father node using the \':hasFather\' property, after ensuring the correct node is assigned the class \':Man\'."\n    },\n    {\n      "explanation": "The current graph incorrectly identifies \'Harriet_Williamina_Hepburn-Forbes\' as the father of \'Charles_Hepburn-Stuart-Forbes-Trefusis_20th\', which conflicts with her classification as a \':Woman\'.",\n      "instruction": "Use RemoveTriple to remove the invalid \':hasFather\' relationship and ensure the correct parent relationship is established using \':hasMother\' if applicable."\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHF8zMF5xy6I2A6W3K41lBydYRFI9wNwec+Xp1rcm8q0KitE+1+daVmhVuX82/'}}]