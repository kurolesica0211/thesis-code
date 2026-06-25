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
    Focus node: Alice_of_Battenberg
    Path: None
    Value: Alice_of_Battenberg
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Man a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
              :Sex,
              :Woman ;
          rdfs:subClassOf [ ] ;
          owl:intersectionOf [ ] ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :Ancestor-hasChild,
              :Ancestor-hasDaughter,
              :Ancestor-hasSon,
              :Ancestor-isAncestorOf,
              :Ancestor-isFatherOf,
              :Ancestor-isMotherOf,
              :Ancestor-isParentOf,
              :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs,
              :Man-hasSex,
              :Man-isBrotherOf,
              :Man-isFatherOf,
              :Man-isSonOf,
              :Man-isUncleOf,
              :Person-hasAncestor,
              :Person-hasBrother,
              :Person-hasFather,
              :Person-hasMother,
              :Person-hasParent,
              :Person-hasRelation,
              :Person-hasSex,
              :Person-hasSister,
              :Person-isBloodrelationOf,
              :Person-isChildOf,
              :Person-isSiblingOf,
              :Person-isSpouseOf ;
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Person .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Woman', ':Person', ':Ancestor', ':Man']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
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
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Classes assigned to the value node: [':Woman', ':Person', ':Ancestor', ':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
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
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: Alice_of_Battenberg
    Path: None
    Value: Alice_of_Battenberg
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Woman a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
              :Man,
              :Sex ;
          rdfs:subClassOf [ ] ;
          owl:intersectionOf [ ] ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :Ancestor-hasChild,
              :Ancestor-hasDaughter,
              :Ancestor-hasSon,
              :Ancestor-isAncestorOf,
              :Ancestor-isFatherOf,
              :Ancestor-isMotherOf,
              :Ancestor-isParentOf,
              :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs,
              :Person-hasAncestor,
              :Person-hasBrother,
              :Person-hasFather,
              :Person-hasMother,
              :Person-hasParent,
              :Person-hasRelation,
              :Person-hasSex,
              :Person-hasSister,
              :Person-isBloodrelationOf,
              :Person-isChildOf,
              :Person-isSiblingOf,
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Person .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Woman', ':Person', ':Ancestor', ':Man']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
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
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Classes assigned to the value node: [':Woman', ':Person', ':Ancestor', ':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
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
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node \'Alice_of_Battenberg\' is incorrectly assigned both the \':Man\' and \':Woman\' classes. These classes are disjoint, meaning an individual cannot be both simultaneously.",\n      "instruction": "Use UnassignClass to remove the \':Man\' class from \'Alice_of_Battenberg\'."\n    },\n    {\n      "explanation": "The node \'Alice_of_Battenberg\' is currently assigned the class \':Man\', which is disjoint with the \':Woman\' class. Since Alice is a woman, the \':Man\' classification is erroneous.",\n      "instruction": "Use UnassignClass to remove the \':Man\' class from \'Alice_of_Battenberg\'."\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHqkCIZZw6/41cbGVAjT0wUih8CMokvjBhWH42Ds1+n6HYTpyk8/emOJtWdkYj'}}]