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
Total violations:29
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Male ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [2]:
    Severity: Violation
    Focus node: Prince_George%2C_Duke_of_Kent
    Path: hasFather
    Value: King_George_V
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [3]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasFather
    Value: Sir_Angus_Ogilvy
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [4]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasMother
    Value: Princess_Alexandra_of_Kent
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [5]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [6]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Male ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [7]:
    Severity: Violation
    Focus node: Princess_Marina_of_Greece_and_Denmark
    Path: hasFather
    Value: Prince_Nicholas_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [8]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasFather
    Value: Sir_Angus_Ogilvy
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [9]:
    Severity: Violation
    Focus node: Prince_George%2C_Duke_of_Kent
    Path: hasFather
    Value: King_George_V
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [10]:
    Severity: Violation
    Focus node: Princess_Alexandra_of_Kent
    Path: hasFather
    Value: Prince_George%2C_Duke_of_Kent
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [11]:
    Severity: Violation
    Focus node: Princess_Marina_of_Greece_and_Denmark
    Path: hasMother
    Value: Grand_Duchess_Elena_Vladimirovna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [12]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasMother
    Value: Princess_Alexandra_of_Kent
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [13]:
    Severity: Violation
    Focus node: Princess_Alexandra_of_Kent
    Path: hasMother
    Value: Princess_Marina_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [14]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [15]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [16]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Male ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [17]:
    Severity: Violation
    Focus node: Princess_Marina_of_Greece_and_Denmark
    Path: hasFather
    Value: Prince_Nicholas_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [18]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasFather
    Value: Sir_Angus_Ogilvy
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [19]:
    Severity: Violation
    Focus node: Prince_George%2C_Duke_of_Kent
    Path: hasFather
    Value: King_George_V
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [20]:
    Severity: Violation
    Focus node: Princess_Alexandra_of_Kent
    Path: hasFather
    Value: Prince_George%2C_Duke_of_Kent
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [21]:
    Severity: Violation
    Focus node: Princess_Marina_of_Greece_and_Denmark
    Path: hasMother
    Value: Grand_Duchess_Elena_Vladimirovna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [22]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasMother
    Value: Princess_Alexandra_of_Kent
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [23]:
    Severity: Violation
    Focus node: Princess_Alexandra_of_Kent
    Path: hasMother
    Value: Princess_Marina_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [24]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [25]:
    Severity: Violation
    Focus node: James_Robert_Bruce_Ogilvy
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Man', ':Person']
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

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
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



  Violation [26]:
    Severity: Violation
    Focus node: Princess_Alexandra_of_Kent
    Path: hasFather
    Value: Prince_George%2C_Duke_of_Kent
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [27]:
    Severity: Violation
    Focus node: Princess_Marina_of_Greece_and_Denmark
    Path: hasFather
    Value: Prince_Nicholas_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man', ':Person']
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



  Violation [28]:
    Severity: Violation
    Focus node: Princess_Alexandra_of_Kent
    Path: hasMother
    Value: Princess_Marina_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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



  Violation [29]:
    Severity: Violation
    Focus node: Princess_Marina_of_Greece_and_Denmark
    Path: hasMother
    Value: Grand_Duchess_Elena_Vladimirovna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman', ':Person']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman', ':Person']
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




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not a valid instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'King_George_V\' for the property :hasFather on node :Prince_George_Duke_of_Kent is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'King_George_V\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Sir_Angus_Ogilvy\' for the property :hasFather on node :James_Robert_Bruce_Ogilvy is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Sir_Angus_Ogilvy\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Princess_Alexandra_of_Kent\' for the property :hasMother on node :James_Robert_Bruce_Ogilvy is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Princess_Alexandra_of_Kent\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Prince_Nicholas_of_Greece_and_Denmark\' for the property :hasFather on node :Princess_Marina_of_Greece_and_Denmark is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Prince_Nicholas_of_Greece_and_Denmark\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Sir_Angus_Ogilvy\' for the property :hasFather on node :James_Robert_Bruce_Ogilvy is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Sir_Angus_Ogilvy\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'King_George_V\' for the property :hasFather on node :Prince_George_Duke_of_Kent is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'King_George_V\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Prince_George_Duke_of_Kent\' for the property :hasFather on node :Princess_Alexandra_of_Kent is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Prince_George_Duke_of_Kent\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Grand_Duchess_Elena_Vladimirovna_of_Russia\' for the property :hasMother on node :Princess_Marina_of_Greece_and_Denmark is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Elena_Vladimirovna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Princess_Alexandra_of_Kent\' for the property :hasMother on node :James_Robert_Bruce_Ogilvy is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Princess_Alexandra_of_Kent\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Princess_Marina_of_Greece_and_Denmark\' for the property :hasMother on node :Princess_Alexandra_of_Kent is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Princess_Marina_of_Greece_and_Denmark\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Prince_Nicholas_of_Greece_and_Denmark\' for the property :hasFather on node :Princess_Marina_of_Greece_and_Denmark is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Prince_Nicholas_of_Greece_and_Denmark\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Sir_Angus_Ogilvy\' for the property :hasFather on node :James_Robert_Bruce_Ogilvy is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Sir_Angus_Ogilvy\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'King_George_V\' for the property :hasFather on node :Prince_George_Duke_of_Kent is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'King_George_V\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Prince_George_Duke_of_Kent\' for the property :hasFather on node :Princess_Alexandra_of_Kent is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Prince_George_Duke_of_Kent\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Grand_Duchess_Elena_Vladimirovna_of_Russia\' for the property :hasMother on node :Princess_Marina_of_Greece_and_Denmark is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Elena_Vladimirovna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Princess_Alexandra_of_Kent\' for the property :hasMother on node :James_Robert_Bruce_Ogilvy is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Princess_Alexandra_of_Kent\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Princess_Marina_of_Greece_and_Denmark\' for the property :hasMother on node :Princess_Alexandra_of_Kent is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Princess_Marina_of_Greece_and_Denmark\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Male\' for the property :hasSex on node :James_Robert_Bruce_Ogilvy is not an instance of the class :Sex.",\n      "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"\n    },\n    {\n      "explanation": "The value \'Prince_George_Duke_of_Kent\' for the property :hasFather on node :Princess_Alexandra_of_Kent is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Prince_George_Duke_of_Kent\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Prince_Nicholas_of_Greece_and_Denmark\' for the property :hasFather on node :Princess_Marina_of_Greece_and_Denmark is not assigned the class :Ancestor or :Man.",\n      "instruction": "AssignClass(node=\'Prince_Nicholas_of_Greece_and_Denmark\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Princess_Marina_of_Greece_and_Denmark\' for the property :hasMother on node :Princess_Alexandra_of_Kent is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Princess_Marina_of_Greece_and_Denmark\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The value \'Grand_Duchess_Elena_Vladimirovna_of_Russia\' for the property :hasMother on node :Princess_Marina_of_Greece_and_Denmark is not assigned the class :Ancestor or :Woman.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Elena_Vladimirovna_of_Russia\', class=\':Ancestor\')"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHUMofD7T7ztS0t2Nl/vp/734hhE5hGpNW0ivV+4s5YM5EF3IIWEyr/6jXK/Kn'}}]