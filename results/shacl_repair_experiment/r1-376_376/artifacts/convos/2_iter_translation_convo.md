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
Total violations:36
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Claire_Booth
    Path: None
    Value: Claire_Booth
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
    Classes assigned to the focus node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .

    Classes assigned to the value node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .



  Violation [2]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: None
    Value: Birgitte_Duchess_of_Gloucester
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
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [3]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasMother
    Value: Birgitte_Duchess_of_Gloucester
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Birgitte_Duchess_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [4]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasFather
    Value: Prince_Richard_Duke_of_Gloucester
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Prince_Richard_Duke_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [5]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasRelation
    Value: Claire_Booth
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Claire_Booth
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasRelation a owl:ObjectProperty,
              owl:SymmetricProperty ;
          rdfs:domain :Person ;
          rdfs:range :Person .
    Classes assigned to the value node: [':Person', ':Woman', ':Female']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [6]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: isSonOf
    Value: Prince_Richard_Duke_of_Gloucester
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Prince_Richard_Duke_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [7]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: isSonOf
    Value: Birgitte_Duchess_of_Gloucester
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Birgitte_Duchess_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [8]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasSex
    Value: Male
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Male
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [9]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: hasSex
    Value: Male
    Constraint: ClosedConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Prince_Richard_Duke_of_Gloucester is closed. It cannot have value: data:Male
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [10]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: None
    Value: Alexander_Patrick_Gregers_Richard_Windsor
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Classes assigned to the value node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [11]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: None
    Value: Prince_Richard_Duke_of_Gloucester
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Male a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Female,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [12]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasMother
    Value: Birgitte_Duchess_of_Gloucester
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
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Birgitte_Duchess_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [13]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasFather
    Value: Prince_Richard_Duke_of_Gloucester
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
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Prince_Richard_Duke_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [14]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasRelation
    Value: Claire_Booth
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
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Claire_Booth
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasRelation a owl:ObjectProperty,
              owl:SymmetricProperty ;
          rdfs:domain :Person ;
          rdfs:range :Person .
    Classes assigned to the value node: [':Person', ':Woman', ':Female']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [15]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: isSonOf
    Value: Prince_Richard_Duke_of_Gloucester
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
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Prince_Richard_Duke_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [16]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: isSonOf
    Value: Birgitte_Duchess_of_Gloucester
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
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Birgitte_Duchess_of_Gloucester
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [17]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: hasSex
    Value: Male
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
    SHACL message: Node data:Alexander_Patrick_Gregers_Richard_Windsor is closed. It cannot have value: data:Male
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [18]:
    Severity: Violation
    Focus node: Claire_Booth
    Path: hasSex
    Value: Female
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
    SHACL message: Node data:Claire_Booth is closed. It cannot have value: data:Female
    Classes assigned to the focus node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .



  Violation [19]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: hasSex
    Value: Female
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
    SHACL message: Node data:Birgitte_Duchess_of_Gloucester is closed. It cannot have value: data:Female
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [20]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: hasSex
    Value: Male
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
    SHACL message: Node data:Prince_Richard_Duke_of_Gloucester is closed. It cannot have value: data:Male
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [21]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: None
    Value: Alexander_Patrick_Gregers_Richard_Windsor
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
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Classes assigned to the value node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [22]:
    Severity: Violation
    Focus node: Claire_Booth
    Path: None
    Value: Claire_Booth
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
    Classes assigned to the focus node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .

    Classes assigned to the value node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .



  Violation [23]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: None
    Value: Birgitte_Duchess_of_Gloucester
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
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [24]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: None
    Value: Prince_Richard_Duke_of_Gloucester
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
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [25]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: None
    Value: Alexander_Patrick_Gregers_Richard_Windsor
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
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Classes assigned to the value node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [26]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: None
    Value: Prince_Richard_Duke_of_Gloucester
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
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [27]:
    Severity: Violation
    Focus node: Claire_Booth
    Path: hasSex
    Value: Female
    Constraint: ClosedConstraintComponent
    Source shape:
      :Female a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Male,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Claire_Booth is closed. It cannot have value: data:Female
    Classes assigned to the focus node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .



  Violation [28]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: hasSex
    Value: Female
    Constraint: ClosedConstraintComponent
    Source shape:
      :Female a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Male,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Node data:Birgitte_Duchess_of_Gloucester is closed. It cannot have value: data:Female
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: [':Sex']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [29]:
    Severity: Violation
    Focus node: Claire_Booth
    Path: None
    Value: Claire_Booth
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Female a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Male,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .

    Classes assigned to the value node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .



  Violation [30]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: None
    Value: Birgitte_Duchess_of_Gloucester
    Constraint: DisjointWithConstraintComponent
    Source shape:
      :Female a rdfs:Class,
              sh:NodeShape ;
          esh:disjointWith :Ancestor,
              :Male,
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
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Sex .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [31]:
    Severity: Violation
    Focus node: Alexander_Patrick_Gregers_Richard_Windsor
    Path: None
    Value: Alexander_Patrick_Gregers_Richard_Windsor
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
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .

    Classes assigned to the value node: [':Man', ':Person', ':Male']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .



  Violation [32]:
    Severity: Violation
    Focus node: Claire_Booth
    Path: None
    Value: Claire_Booth
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
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .

    Classes assigned to the value node: [':Person', ':Woman', ':Female']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .



  Violation [33]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: None
    Value: Birgitte_Duchess_of_Gloucester
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
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [34]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: None
    Value: Prince_Richard_Duke_of_Gloucester
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
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [35]:
    Severity: Violation
    Focus node: Prince_Richard_Duke_of_Gloucester
    Path: None
    Value: Prince_Richard_Duke_of_Gloucester
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
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Person .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Man', ':Person', ':Male', ':Ancestor']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
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
      Class :Male:
        :Male a owl:Class ;
            rdfs:subClassOf :Sex .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .



  Violation [36]:
    Severity: Violation
    Focus node: Birgitte_Duchess_of_Gloucester
    Path: None
    Value: Birgitte_Duchess_of_Gloucester
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
              :Woman-isAuntOf,
              :Woman-isDaughterOf,
              :Woman-isMotherOf,
              :Woman-isSisterOf ;
          sh:rule esh:InferTypeRule_DomainEntity,
              esh:InferTypeRule_Person .
    SHACL message: Class disjointness violation.
    Classes assigned to the focus node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
      Class :Ancestor:
        :Ancestor a owl:Class ;
            owl:disjointWith :Sex ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :isAncestorOf ;
                                owl:someValuesFrom :Person ] ) ] .

    Classes assigned to the value node: [':Person', ':Woman', ':Female', ':Ancestor']
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
      Class :Female:
        :Female a owl:Class ;
            rdfs:subClassOf :Sex ;
            owl:disjointWith :Male .
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

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Claire_Booth has conflicting class assignments. It is assigned to :Woman and :Female, which are defined as disjoint from each other in the schema.",\n      "instruction": "Use UnassignClass to remove the :Female class from Claire_Booth."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester has conflicting class assignments. It is assigned to :Woman and :Female, which are defined as disjoint from each other in the schema.",\n      "instruction": "Use UnassignClass to remove the :Female class from Birgitte_Duchess_of_Gloucester."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is marked as a closed shape, meaning it cannot have the property :hasMother pointing to Birgitte_Duchess_of_Gloucester.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Birgitte_Duchess_of_Gloucester via :hasMother."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is marked as a closed shape, meaning it cannot have the property :hasFather pointing to Prince_Richard_Duke_of_Gloucester.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Prince_Richard_Duke_of_Gloucester via :hasFather."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is marked as a closed shape, meaning it cannot have the property :hasRelation pointing to Claire_Booth.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Claire_Booth via :hasRelation."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is marked as a closed shape, meaning it cannot have the property :isSonOf pointing to Prince_Richard_Duke_of_Gloucester.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Prince_Richard_Duke_of_Gloucester via :isSonOf."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is marked as a closed shape, meaning it cannot have the property :isSonOf pointing to Birgitte_Duchess_of_Gloucester.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Birgitte_Duchess_of_Gloucester via :isSonOf."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is marked as a closed shape, meaning it cannot have the property :hasSex pointing to Male.",\n      "instruction": "Use RemoveLiteral to remove the Male value from :hasSex for the node Alexander_Patrick_Gregers_Richard_Windsor."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester is marked as a closed shape, meaning it cannot have the property :hasSex pointing to Male.",\n      "instruction": "Use RemoveLiteral to remove the Male value from :hasSex for the node Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor has conflicting class assignments. It is assigned to :Man and :Male, which are defined as disjoint.",\n      "instruction": "Use UnassignClass to remove the :Male class from Alexander_Patrick_Gregers_Richard_Windsor."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester has conflicting class assignments. It is assigned to :Man and :Male, which are defined as disjoint.",\n      "instruction": "Use UnassignClass to remove the :Male class from Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is closed and cannot have the property :hasMother pointing to Birgitte_Duchess_of_Gloucester under the current shape configuration.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Birgitte_Duchess_of_Gloucester via :hasMother."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is closed and cannot have the property :hasFather pointing to Prince_Richard_Duke_of_Gloucester under the current shape configuration.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Prince_Richard_Duke_of_Gloucester via :hasFather."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is closed and cannot have the property :hasRelation pointing to Claire_Booth under the current shape configuration.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Claire_Booth via :hasRelation."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is closed and cannot have the property :isSonOf pointing to Prince_Richard_Duke_of_Gloucester under the current shape configuration.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Prince_Richard_Duke_of_Gloucester via :isSonOf."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is closed and cannot have the property :isSonOf pointing to Birgitte_Duchess_of_Gloucester under the current shape configuration.",\n      "instruction": "Use RemoveTriple to delete the relationship between Alexander_Patrick_Gregers_Richard_Windsor and Birgitte_Duchess_of_Gloucester via :isSonOf."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor is closed and cannot have the property :hasSex pointing to Male under the current shape configuration.",\n      "instruction": "Use RemoveLiteral to remove the Male value from :hasSex for the node Alexander_Patrick_Gregers_Richard_Windsor."\n    },\n    {\n      "explanation": "The node Claire_Booth is closed and cannot have the property :hasSex pointing to Female under the current shape configuration.",\n      "instruction": "Use RemoveLiteral to remove the Female value from :hasSex for the node Claire_Booth."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester is closed and cannot have the property :hasSex pointing to Female under the current shape configuration.",\n      "instruction": "Use RemoveLiteral to remove the Female value from :hasSex for the node Birgitte_Duchess_of_Gloucester."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester is closed and cannot have the property :hasSex pointing to Male under the current shape configuration.",\n      "instruction": "Use RemoveLiteral to remove the Male value from :hasSex for the node Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Alexander_Patrick_Gregers_Richard_Windsor."\n    },\n    {\n      "explanation": "The node Claire_Booth has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Claire_Booth."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Birgitte_Duchess_of_Gloucester."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Alexander_Patrick_Gregers_Richard_Windsor."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Claire_Booth is closed and cannot have the property :hasSex pointing to Female.",\n      "instruction": "Use RemoveLiteral to remove the Female value from :hasSex for the node Claire_Booth."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester is closed and cannot have the property :hasSex pointing to Female.",\n      "instruction": "Use RemoveLiteral to remove the Female value from :hasSex for the node Birgitte_Duchess_of_Gloucester."\n    },\n    {\n      "explanation": "The node Claire_Booth has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Claire_Booth."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Birgitte_Duchess_of_Gloucester."\n    },\n    {\n      "explanation": "The node Alexander_Patrick_Gregers_Richard_Windsor has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Alexander_Patrick_Gregers_Richard_Windsor."\n    },\n    {\n      "explanation": "The node Claire_Booth has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Claire_Booth."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Birgitte_Duchess_of_Gloucester."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Prince_Richard_Duke_of_Gloucester has conflicting class assignments between :Man and :Male.",\n      "instruction": "Use UnassignClass to remove the :Male class from Prince_Richard_Duke_of_Gloucester."\n    },\n    {\n      "explanation": "The node Birgitte_Duchess_of_Gloucester has conflicting class assignments between :Woman and :Female.",\n      "instruction": "Use UnassignClass to remove the :Female class from Birgitte_Duchess_of_Gloucester."\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgERTTIPZvDPMSNTLanM3NFQFxKWkfP+6DOF4PXdgVBJxk2nQ93TzP/DgCd1xYdfanCX'}}]