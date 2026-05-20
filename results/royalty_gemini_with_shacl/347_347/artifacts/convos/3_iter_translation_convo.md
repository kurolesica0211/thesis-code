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
Total violations:23
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Sarah_Georgina_Walker
    Path: None
    Value: Sarah_Georgina_Walker
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Ancestor a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
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
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Person .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Path: None
    Value: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Ancestor a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
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
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Person .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [3]:
    Severity: Violation
    Focus node: Henry_Mountbatten_Earl_of_Medina
    Path: None
    Value: Henry_Mountbatten_Earl_of_Medina
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
    Classes assigned to the focus node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [4]:
    Severity: Violation
    Focus node: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Path: None
    Value: George_Mountbatten_4th_Marquess_of_Milford_Haven
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
    Classes assigned to the focus node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [5]:
    Severity: Violation
    Focus node: Henry_Mountbatten_Earl_of_Medina
    Path: hasParent
    Value: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Henry_Mountbatten_Earl_of_Medina is closed. It cannot have value: data:George_Mountbatten_4th_Marquess_of_Milford_Haven
    Classes assigned to the focus node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [6]:
    Severity: Violation
    Focus node: Henry_Mountbatten_Earl_of_Medina
    Path: hasParent
    Value: Sarah_Georgina_Walker
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Henry_Mountbatten_Earl_of_Medina is closed. It cannot have value: data:Sarah_Georgina_Walker
    Classes assigned to the focus node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [7]:
    Severity: Violation
    Focus node: Henry_Mountbatten_Earl_of_Medina
    Path: hasSex
    Value: Male_Sex
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Henry_Mountbatten_Earl_of_Medina is closed. It cannot have value: data:Male_Sex
    Classes assigned to the focus node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Male']
    Definitions of the classes assigned to the value node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [8]:
    Severity: Violation
    Focus node: Sarah_Georgina_Walker
    Path: hasSex
    Value: Female_Sex
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Sarah_Georgina_Walker is closed. It cannot have value: data:Female_Sex
    Classes assigned to the focus node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Female']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [9]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: hasMother
    Value: Sarah_Georgina_Walker
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Lady_Tatiana_Mountbatten is closed. It cannot have value: data:Sarah_Georgina_Walker
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [10]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: hasBrother
    Value: Henry_Mountbatten_Earl_of_Medina
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Lady_Tatiana_Mountbatten is closed. It cannot have value: data:Henry_Mountbatten_Earl_of_Medina
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasBrother a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Man ;
          rdfs:subPropertyOf :isSiblingOf ;
          owl:inverseOf :isBrotherOf ;
          owl:propertyDisjointWith :isChildOf,
              :isParentOf .
    Classes assigned to the value node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [11]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: hasFather
    Value: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Lady_Tatiana_Mountbatten is closed. It cannot have value: data:George_Mountbatten_4th_Marquess_of_Milford_Haven
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [12]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: hasSex
    Value: Female_Sex
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:Lady_Tatiana_Mountbatten is closed. It cannot have value: data:Female_Sex
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Female']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [13]:
    Severity: Violation
    Focus node: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Path: hasSex
    Value: Male_Sex
    Constraint: ClosedConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Node data:George_Mountbatten_4th_Marquess_of_Milford_Haven is closed. It cannot have value: data:Male_Sex
    Classes assigned to the focus node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Male']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [14]:
    Severity: Violation
    Focus node: Henry_Mountbatten_Earl_of_Medina
    Path: None
    Value: Henry_Mountbatten_Earl_of_Medina
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [15]:
    Severity: Violation
    Focus node: Sarah_Georgina_Walker
    Path: None
    Value: Sarah_Georgina_Walker
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [16]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: None
    Value: Lady_Tatiana_Mountbatten
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [17]:
    Severity: Violation
    Focus node: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Path: None
    Value: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Sex a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Man,
              :Person,
              :Woman ;
          sh:closed true ;
          sh:ignoredProperties ( rdf:type ) ;
          sh:property :AnnotationProperty_alsoKnownAs,
              :AnnotationProperty_formerlyKnownAs,
              :AnnotationProperty_hasBirthYear,
              :AnnotationProperty_hasDeathYear,
              :AnnotationProperty_hasMarriageYear,
              :AnnotationProperty_knownAs ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [18]:
    Severity: Violation
    Focus node: Henry_Mountbatten_Earl_of_Medina
    Path: None
    Value: Henry_Mountbatten_Earl_of_Medina
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Person a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
              :Sex ;
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
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [19]:
    Severity: Violation
    Focus node: Sarah_Georgina_Walker
    Path: None
    Value: Sarah_Georgina_Walker
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Person a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
              :Sex ;
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
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [20]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: None
    Value: Lady_Tatiana_Mountbatten
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Person a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
              :Sex ;
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
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [21]:
    Severity: Violation
    Focus node: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Path: None
    Value: George_Mountbatten_4th_Marquess_of_Milford_Haven
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Person a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Female,
              :Male,
              :Sex ;
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
              :Person-isSpouseOf,
              :Woman-hasSex,
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Man', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [22]:
    Severity: Violation
    Focus node: Sarah_Georgina_Walker
    Path: None
    Value: Sarah_Georgina_Walker
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
    Classes assigned to the focus node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Ancestor', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .



  Violation [23]:
    Severity: Violation
    Focus node: Lady_Tatiana_Mountbatten
    Path: None
    Value: Lady_Tatiana_Mountbatten
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
    Classes assigned to the focus node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the focus node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Sex']
    Definitions of the classes assigned to the value node:
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
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .
      Class :Sex:
        :Sex a owl:Class ;
            rdfs:subClassOf :DomainEntity ;
            owl:equivalentClass [ a owl:Class ;
                    owl:unionOf ( :Female :Male ) ] .




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Sarah_Georgina_Walker has been assigned conflicting classes that are defined as disjoint, specifically :Sex and :Person/:Woman.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Sarah_Georgina_Walker."\n    },\n    {\n      "explanation": "The node George_Mountbatten_4th_Marquess_of_Milford_Haven has been assigned conflicting classes that are defined as disjoint, specifically :Sex and :Person/:Man.",\n      "instruction": "Use UnassignClass to remove the :Sex class from George_Mountbatten_4th_Marquess_of_Milford_Haven."\n    },\n    {\n      "explanation": "The node Henry_Mountbatten_Earl_of_Medina has been assigned conflicting classes that are defined as disjoint, specifically :Sex and :Person/:Man.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Henry_Mountbatten_Earl_of_Medina."\n    },\n    {\n      "explanation": "The node George_Mountbatten_4th_Marquess_of_Milford_Haven has been assigned conflicting classes that are defined as disjoint, specifically :Sex and :Person/:Man.",\n      "instruction": "Use UnassignClass to remove the :Sex class from George_Mountbatten_4th_Marquess_of_Milford_Haven."\n    },\n    {\n      "explanation": "The node Henry_Mountbatten_Earl_of_Medina is marked as a :Sex, which is a closed shape and does not permit the \'hasParent\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Henry_Mountbatten_Earl_of_Medina."\n    },\n    {\n      "explanation": "The node Henry_Mountbatten_Earl_of_Medina is marked as a :Sex, which is a closed shape and does not permit the \'hasParent\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Henry_Mountbatten_Earl_of_Medina."\n    },\n    {\n      "explanation": "The node Henry_Mountbatten_Earl_of_Medina is marked as a :Sex, which is a closed shape and does not permit the \'hasSex\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Henry_Mountbatten_Earl_of_Medina."\n    },\n    {\n      "explanation": "The node Sarah_Georgina_Walker is marked as a :Sex, which is a closed shape and does not permit the \'hasSex\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Sarah_Georgina_Walker."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten is incorrectly assigned the :Sex class, which is a closed shape that does not allow the \'hasMother\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten is incorrectly assigned the :Sex class, which is a closed shape that does not allow the \'hasBrother\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten is incorrectly assigned the :Sex class, which is a closed shape that does not allow the \'hasFather\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten is incorrectly assigned the :Sex class, which is a closed shape that does not allow the \'hasSex\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    },\n    {\n      "explanation": "The node George_Mountbatten_4th_Marquess_of_Milford_Haven is incorrectly assigned the :Sex class, which is a closed shape that does not allow the \'hasSex\' relationship.",\n      "instruction": "Use UnassignClass to remove the :Sex class from George_Mountbatten_4th_Marquess_of_Milford_Haven."\n    },\n    {\n      "explanation": "The node Henry_Mountbatten_Earl_of_Medina has conflicting class assignments as it is labeled as both :Sex and :Person/:Man.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Henry_Mountbatten_Earl_of_Medina."\n    },\n    {\n      "explanation": "The node Sarah_Georgina_Walker has conflicting class assignments as it is labeled as both :Sex and :Person/:Woman.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Sarah_Georgina_Walker."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten has conflicting class assignments as it is labeled as both :Sex and :Person/:Woman.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    },\n    {\n      "explanation": "The node George_Mountbatten_4th_Marquess_of_Milford_Haven has conflicting class assignments as it is labeled as both :Sex and :Person/:Man.",\n      "instruction": "Use UnassignClass to remove the :Sex class from George_Mountbatten_4th_Marquess_of_Milford_Haven."\n    },\n    {\n      "explanation": "The node Henry_Mountbatten_Earl_of_Medina has conflicting class assignments as it is labeled as both :Sex and :Person.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Henry_Mountbatten_Earl_of_Medina."\n    },\n    {\n      "explanation": "The node Sarah_Georgina_Walker has conflicting class assignments as it is labeled as both :Sex and :Person.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Sarah_Georgina_Walker."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten has conflicting class assignments as it is labeled as both :Sex and :Person.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    },\n    {\n      "explanation": "The node George_Mountbatten_4th_Marquess_of_Milford_Haven has conflicting class assignments as it is labeled as both :Sex and :Person.",\n      "instruction": "Use UnassignClass to remove the :Sex class from George_Mountbatten_4th_Marquess_of_Milford_Haven."\n    },\n    {\n      "explanation": "The node Sarah_Georgina_Walker has conflicting class assignments as it is labeled as both :Sex and :Woman.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Sarah_Georgina_Walker."\n    },\n    {\n      "explanation": "The node Lady_Tatiana_Mountbatten has conflicting class assignments as it is labeled as both :Sex and :Woman.",\n      "instruction": "Use UnassignClass to remove the :Sex class from Lady_Tatiana_Mountbatten."\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHPgRPcwpFG94YxdLySLHWAyo5z9DFHpcAfl63Sg8XgFrqT47R49ZLE3a5a+1I'}}]