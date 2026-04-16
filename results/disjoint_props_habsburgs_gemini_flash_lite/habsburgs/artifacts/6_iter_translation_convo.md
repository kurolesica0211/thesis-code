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
Total violations:3
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Rudolf_II
    Path: isSiblingOf
    Value: Albert_I
    Constraint: ClosedConstraintComponent
    Source shape:
      :DomainEntity a rdfs:Class,
              sh:NodeShape ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :DomainEntity-alsoKnownAs,
              :DomainEntity-formerlyKnownAs,
              :DomainEntity-hasBirthYear,
              :DomainEntity-hasDeathYear,
              :DomainEntity-hasMarriageYear,
              :DomainEntity-knownAs .
    SHACL message: Node data:Rudolf_II is closed. It cannot have value: data:Albert_I

    Classes assigned to the focus node: [':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
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
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .

    Definition of the path:
      :isSiblingOf a owl:ObjectProperty,
              owl:SymmetricProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Person ;
          rdfs:subPropertyOf :isBloodrelationOf ;
          owl:propertyChainAxiom ( :hasParent :isParentOf ) ;
          owl:propertyDisjointWith ( :isParentOf :isChildOf ) .
    Classes assigned to the value node: [':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
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
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .




  Violation [2]:
    Severity: Violation
    Focus node: Albert_I
    Path: isFatherOf
    Value: Rudolf_II
    Constraint: ClosedConstraintComponent
    Source shape:
      :DomainEntity a rdfs:Class,
              sh:NodeShape ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :DomainEntity-alsoKnownAs,
              :DomainEntity-formerlyKnownAs,
              :DomainEntity-hasBirthYear,
              :DomainEntity-hasDeathYear,
              :DomainEntity-hasMarriageYear,
              :DomainEntity-knownAs .
    SHACL message: Node data:Albert_I is closed. It cannot have value: data:Rudolf_II

    Classes assigned to the focus node: [':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
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
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .

    Definition of the path:
      :isFatherOf a owl:ObjectProperty ;
          rdfs:domain :Ancestor,
              :Man ;
          rdfs:range :Person ;
          rdfs:subPropertyOf :hasChild,
              :isParentOf .
    Classes assigned to the value node: [':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
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
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .




  Violation [3]:
    Severity: Violation
    Focus node: Guntram_the_Rich
    Path: isBrotherOf
    Value: Radbot
    Constraint: ClosedConstraintComponent
    Source shape:
      :DomainEntity a rdfs:Class,
              sh:NodeShape ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :DomainEntity-alsoKnownAs,
              :DomainEntity-formerlyKnownAs,
              :DomainEntity-hasBirthYear,
              :DomainEntity-hasDeathYear,
              :DomainEntity-hasMarriageYear,
              :DomainEntity-knownAs .
    SHACL message: Node data:Guntram_the_Rich is closed. It cannot have value: data:Radbot

    Classes assigned to the focus node: [':Man', ':Person']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
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
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .

    Definition of the path:
      :isBrotherOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Person ;
          rdfs:subPropertyOf :isSiblingOf .
    Classes assigned to the value node: [':Man', ':Person']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Marriage,
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
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Man :Woman ) ] .





---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node \'Rudolf_II\' is defined as a closed shape, meaning it cannot contain the property \'isSiblingOf\' as it is not listed in the allowed properties for \'DomainEntity\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \'Rudolf_II\' :isSiblingOf \'Albert_I\'."\n    },\n    {\n      "explanation": "The node \'Albert_I\' is defined as a closed shape, meaning it cannot contain the property \'isFatherOf\' as it is not listed in the allowed properties for \'DomainEntity\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \'Albert_I\' :isFatherOf \'Rudolf_II\'."\n    },\n    {\n      "explanation": "The node \'Guntram_the_Rich\' is defined as a closed shape, meaning it cannot contain the property \'isBrotherOf\' as it is not listed in the allowed properties for \'DomainEntity\'.",\n      "instruction": "Use RemoveTriple to delete the relationship \'Guntram_the_Rich\' :isBrotherOf \'Radbot\'."\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbH9oNSGpvusCVFpiMhSMlALbp6LvbzUveCMAwPSRynvTq1a5CBC0h6UvmO8scy'}}]