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
Total violations:33
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Louis_Philippe_I
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [2]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Philippe_I_Duke_of_Orleans
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Louis_XIV
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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
    Focus node: Philippe_I_Duke_of_Orleans
    Path: hasFather
    Value: Louis_XIII
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



  Violation [5]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasFather
    Value: Jean_Duke_of_Guise
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



  Violation [6]:
    Severity: Violation
    Focus node: Michel
    Path: hasFather
    Value: Henri_dOrleans
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



  Violation [7]:
    Severity: Violation
    Focus node: Henri_son_of_Henri
    Path: hasFather
    Value: Henri_dOrleans
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



  Violation [8]:
    Severity: Violation
    Focus node: Thibaut
    Path: hasFather
    Value: Henri_dOrleans
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
    Focus node: Henri_dOrleans
    Path: hasMother
    Value: Philippe_Duke_of_Orleans
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
    Focus node: Henri_dOrleans
    Path: hasMother
    Value: Philippe_Duke_of_Orleans
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



  Violation [11]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Louis_Philippe_I
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [12]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Philippe_I_Duke_of_Orleans
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [13]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Louis_XIV
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [14]:
    Severity: Violation
    Focus node: Philippe_I_Duke_of_Orleans
    Path: hasFather
    Value: Louis_XIII
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



  Violation [15]:
    Severity: Violation
    Focus node: Francoise_Marie_de_Bourbon
    Path: hasFather
    Value: Louis_XIV
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



  Violation [16]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasFather
    Value: Jean_Duke_of_Guise
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



  Violation [17]:
    Severity: Violation
    Focus node: Michel
    Path: hasFather
    Value: Henri_dOrleans
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



  Violation [18]:
    Severity: Violation
    Focus node: Henri_son_of_Henri
    Path: hasFather
    Value: Henri_dOrleans
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
    Focus node: Thibaut
    Path: hasFather
    Value: Henri_dOrleans
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
    Focus node: Henri_dOrleans
    Path: hasMother
    Value: Philippe_Duke_of_Orleans
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



  Violation [21]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasMother
    Value: Philippe_Duke_of_Orleans
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



  Violation [22]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Louis_Philippe_I
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [23]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Philippe_I_Duke_of_Orleans
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [24]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasAncestor
    Value: Louis_XIV
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasAncestor a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :hasAncestor .
    SHACL message: Value does not have class :Ancestor
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
      :hasAncestor a owl:ObjectProperty,
              owl:TransitiveProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasRelation,
              owl:topObjectProperty ;
          owl:inverseOf :isAncestorOf .
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



  Violation [25]:
    Severity: Violation
    Focus node: Philippe_I_Duke_of_Orleans
    Path: hasFather
    Value: Louis_XIII
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



  Violation [26]:
    Severity: Violation
    Focus node: Francoise_Marie_de_Bourbon
    Path: hasFather
    Value: Louis_XIV
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
    Focus node: Henri_dOrleans
    Path: hasFather
    Value: Jean_Duke_of_Guise
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



  Violation [28]:
    Severity: Violation
    Focus node: Michel
    Path: hasFather
    Value: Henri_dOrleans
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



  Violation [29]:
    Severity: Violation
    Focus node: Henri_son_of_Henri
    Path: hasFather
    Value: Henri_dOrleans
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



  Violation [30]:
    Severity: Violation
    Focus node: Thibaut
    Path: hasFather
    Value: Henri_dOrleans
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



  Violation [31]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasMother
    Value: Philippe_Duke_of_Orleans
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



  Violation [32]:
    Severity: Violation
    Focus node: Henri_dOrleans
    Path: hasMother
    Value: Philippe_Duke_of_Orleans
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



  Violation [33]:
    Severity: Violation
    Focus node: Francoise_Marie_de_Bourbon
    Path: hasFather
    Value: Louis_XIV
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




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {"explanation": "The ancestor Louis_Philippe_I for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_Philippe_I, :Ancestor)"},\n    {"explanation": "The ancestor Philippe_I_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_I_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The ancestor Louis_XIV for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIV, :Ancestor)"},\n    {"explanation": "The father Louis_XIII for Philippe_I_Duke_of_Orleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIII, :Ancestor)"},\n    {"explanation": "The father Jean_Duke_of_Guise for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Jean_Duke_of_Guise, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Michel is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Henri_son_of_Henri is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Thibaut is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The mother Philippe_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The mother Philippe_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The ancestor Louis_Philippe_I for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_Philippe_I, :Ancestor)"},\n    {"explanation": "The ancestor Philippe_I_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_I_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The ancestor Louis_XIV for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIV, :Ancestor)"},\n    {"explanation": "The father Louis_XIII for Philippe_I_Duke_of_Orleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIII, :Ancestor)"},\n    {"explanation": "The father Louis_XIV for Francoise_Marie_de_Bourbon is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIV, :Ancestor)"},\n    {"explanation": "The father Jean_Duke_of_Guise for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Jean_Duke_of_Guise, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Michel is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Henri_son_of_Henri is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Thibaut is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The mother Philippe_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The mother Philippe_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The ancestor Louis_Philippe_I for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_Philippe_I, :Ancestor)"},\n    {"explanation": "The ancestor Philippe_I_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_I_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The ancestor Louis_XIV for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIV, :Ancestor)"},\n    {"explanation": "The father Louis_XIII for Philippe_I_Duke_of_Orleans is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIII, :Ancestor)"},\n    {"explanation": "The father Louis_XIV for Francoise_Marie_de_Bourbon is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIV, :Ancestor)"},\n    {"explanation": "The father Jean_Duke_of_Guise for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Jean_Duke_of_Guise, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Michel is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Henri_son_of_Henri is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The father Henri_dOrleans for Thibaut is missing the required :Ancestor class.", "instruction": "AssignClass(Henri_dOrleans, :Ancestor)"},\n    {"explanation": "The mother Philippe_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The mother Philippe_Duke_of_Orleans for Henri_dOrleans is missing the required :Ancestor class.", "instruction": "AssignClass(Philippe_Duke_of_Orleans, :Ancestor)"},\n    {"explanation": "The father Louis_XIV for Francoise_Marie_de_Bourbon is missing the required :Ancestor class.", "instruction": "AssignClass(Louis_XIV, :Ancestor)"}\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHy1rMMyay59sMSiYULLWMB97Nu6U3UhVg9osLchEjeB/vxB2u3plns7cY9bCj'}}]