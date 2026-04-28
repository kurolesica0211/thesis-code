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
    Focus node: George_VI
    Path: hasHusband
    Value: Queen_Elizabeth_The_Queen_Mother
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasHusband a sh:PropertyShape ;
          sh:class :Man ;
          sh:path :hasHusband .
    SHACL message: Value does not have class :Man

    Classes assigned to the focus node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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

    Definition of the path:
      :hasHusband a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Man ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isHusbandOf ;
          owl:propertyChainAxiom ( :isFemalePartnerIn :hasMalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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




  Violation [2]:
    Severity: Violation
    Focus node: George_VI
    Path: hasHusband
    Value: Queen_Elizabeth_The_Queen_Mother
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasHusband a sh:PropertyShape ;
          sh:class :Man ;
          sh:path :hasHusband .
    SHACL message: Value does not have class :Man

    Classes assigned to the focus node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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

    Definition of the path:
      :hasHusband a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Man ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isHusbandOf ;
          owl:propertyChainAxiom ( :isFemalePartnerIn :hasMalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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




  Violation [3]:
    Severity: Violation
    Focus node: George_VI
    Path: hasHusband
    Value: Queen_Elizabeth_The_Queen_Mother
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasHusband a sh:PropertyShape ;
          sh:class :Man ;
          sh:path :hasHusband .
    SHACL message: Value does not have class :Man

    Classes assigned to the focus node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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

    Definition of the path:
      :hasHusband a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Man ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isHusbandOf ;
          owl:propertyChainAxiom ( :isFemalePartnerIn :hasMalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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




  Violation [4]:
    Severity: Violation
    Focus node: George_VI
    Path: hasHusband
    Value: Queen_Elizabeth_The_Queen_Mother
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasHusband a sh:PropertyShape ;
          sh:class :Man ;
          sh:path :hasHusband .
    SHACL message: Value does not have class :Man

    Classes assigned to the focus node: [':Ancestor', ':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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

    Definition of the path:
      :hasHusband a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Man ;
          rdfs:subPropertyOf :hasSpouse ;
          owl:inverseOf :isHusbandOf ;
          owl:propertyChainAxiom ( :isFemalePartnerIn :hasMalePartner ) .
    Classes assigned to the value node: [':Ancestor', ':Person', ':Woman']
    Definitions of the classes assigned to the value node:
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
                :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
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





---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node George_VI has a \'hasHusband\' relationship pointing to \'Queen_Elizabeth_The_Queen_Mother\', but the property definition requires the target to be a member of the class \':Man\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \':George_VI :hasHusband :Queen_Elizabeth_The_Queen_Mother\'."\n    },\n    {\n      "explanation": "The node George_VI has a \'hasHusband\' relationship pointing to \'Queen_Elizabeth_The_Queen_Mother\', but the property definition requires the target to be a member of the class \':Man\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \':George_VI :hasHusband :Queen_Elizabeth_The_Queen_Mother\'."\n    },\n    {\n      "explanation": "The node George_VI has a \'hasHusband\' relationship pointing to \'Queen_Elizabeth_The_Queen_Mother\', but the property definition requires the target to be a member of the class \':Man\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \':George_VI :hasHusband :Queen_Elizabeth_The_Queen_Mother\'."\n    },\n    {\n      "explanation": "The node George_VI has a \'hasHusband\' relationship pointing to \'Queen_Elizabeth_The_Queen_Mother\', but the property definition requires the target to be a member of the class \':Man\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \':George_VI :hasHusband :Queen_Elizabeth_The_Queen_Mother\'."\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHzQygRElctk7TnOAEM+V0u5Xcp+Cp8Kt8VCKKOHb4F/3EcZdJub9rz11ZCqs6'}}]