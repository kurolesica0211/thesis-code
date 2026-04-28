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
    Focus node: Queen_Elizabeth_The_Queen_Mother
    Path: hasWife
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasWife a sh:PropertyShape ;
          sh:class :Woman ;
          sh:path :hasWife .
    SHACL message: Value does not have class :Woman

    Classes assigned to the focus node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasWife a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isWifeOf ;
          owl:propertyChainAxiom ( :isMalePartnerIn :hasFemalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .




  Violation [2]:
    Severity: Violation
    Focus node: Queen_Elizabeth_The_Queen_Mother
    Path: hasWife
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasWife a sh:PropertyShape ;
          sh:class :Woman ;
          sh:path :hasWife .
    SHACL message: Value does not have class :Woman

    Classes assigned to the focus node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasWife a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isWifeOf ;
          owl:propertyChainAxiom ( :isMalePartnerIn :hasFemalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .




  Violation [3]:
    Severity: Violation
    Focus node: Queen_Elizabeth_The_Queen_Mother
    Path: hasWife
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasWife a sh:PropertyShape ;
          sh:class :Woman ;
          sh:path :hasWife .
    SHACL message: Value does not have class :Woman

    Classes assigned to the focus node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasWife a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isWifeOf ;
          owl:propertyChainAxiom ( :isMalePartnerIn :hasFemalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .




  Violation [4]:
    Severity: Violation
    Focus node: Queen_Elizabeth_The_Queen_Mother
    Path: hasWife
    Value: George_VI
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasWife a sh:PropertyShape ;
          sh:class :Woman ;
          sh:path :hasWife .
    SHACL message: Value does not have class :Woman

    Classes assigned to the focus node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasWife a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isWifeOf ;
          owl:propertyChainAxiom ( :isMalePartnerIn :hasFemalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Person:
        :Person a owl:Class ;
            rdfs:subClassOf [ a owl:Restriction ;
                    owl:onProperty :hasFather ;
                    owl:someValuesFrom :Man ],
                [ a owl:Restriction ;
                    owl:onProperty :hasMother ;
                    owl:someValuesFrom :Woman ],
                [ a owl:Restriction ;
                    owl:onProperty :hasSex ;
                    owl:someValuesFrom :Sex ],
                [ a owl:Restriction ;
                    owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
                    owl:onClass :Person ;
                    owl:onProperty :hasParent ],
                :DomainEntity ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .





---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node \'Queen_Elizabeth_The_Queen_Mother\' has a \'hasWife\' relationship pointing to \'George_VI\', but \'George_VI\' is not classified as a \'Woman\', which is required for this property.",\n      "instruction": "RemoveTriple(Queen_Elizabeth_The_Queen_Mother, hasWife, George_VI)"\n    },\n    {\n      "explanation": "The node \'Queen_Elizabeth_The_Queen_Mother\' has a \'hasWife\' relationship pointing to \'George_VI\', but \'George_VI\' is not classified as a \'Woman\', which is required for this property.",\n      "instruction": "RemoveTriple(Queen_Elizabeth_The_Queen_Mother, hasWife, George_VI)"\n    },\n    {\n      "explanation": "The node \'Queen_Elizabeth_The_Queen_Mother\' has a \'hasWife\' relationship pointing to \'George_VI\', but \'George_VI\' is not classified as a \'Woman\', which is required for this property.",\n      "instruction": "RemoveTriple(Queen_Elizabeth_The_Queen_Mother, hasWife, George_VI)"\n    },\n    {\n      "explanation": "The node \'Queen_Elizabeth_The_Queen_Mother\' has a \'hasWife\' relationship pointing to \'George_VI\', but \'George_VI\' is not classified as a \'Woman\', which is required for this property.",\n      "instruction": "RemoveTriple(Queen_Elizabeth_The_Queen_Mother, hasWife, George_VI)"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHabfPMyKAW/pTqBeBYG19pgg8JIRygMQdbav7Np8NsqRnBZyySBJCLAIi+BX2'}}]