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
Total violations:27
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: David_Nightingale_Hicks
    Path: hasFather
    Value: Herbert_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [2]:
    Severity: Violation
    Focus node: Louis_Mountbatten
    Path: hasFather
    Value: Prince_Louis_of_Battenberg
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [3]:
    Severity: Violation
    Focus node: David_Nightingale_Hicks
    Path: hasMother
    Value: Iris_Elsie_Platten
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [4]:
    Severity: Violation
    Focus node: Louis_Mountbatten
    Path: hasMother
    Value: Princess_Victoria_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [5]:
    Severity: Violation
    Focus node: Edwina_Ashley
    Path: hasFather
    Value: Baron_Mount_Temple
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [6]:
    Severity: Violation
    Focus node: Pamela_Hicks
    Path: hasFather
    Value: Louis_Mountbatten
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [7]:
    Severity: Violation
    Focus node: David_Nightingale_Hicks
    Path: hasFather
    Value: Herbert_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [8]:
    Severity: Violation
    Focus node: Louis_Mountbatten
    Path: hasFather
    Value: Prince_Louis_of_Battenberg
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [9]:
    Severity: Violation
    Focus node: Pamela_Hicks
    Path: hasMother
    Value: Edwina_Ashley
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [10]:
    Severity: Violation
    Focus node: David_Nightingale_Hicks
    Path: hasMother
    Value: Iris_Elsie_Platten
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [11]:
    Severity: Violation
    Focus node: Louis_Mountbatten
    Path: hasMother
    Value: Princess_Victoria_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [12]:
    Severity: Violation
    Focus node: India_Hicks
    Path: isChildOf
    Value: David_Nightingale_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-isChildOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:disjoint :hasBrother,
              :hasSister,
              :isBrotherOf,
              :isSisterOf ;
          sh:path :isChildOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :isChildOf a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:propertyDisjointWith :isSisterOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [13]:
    Severity: Violation
    Focus node: India_Hicks
    Path: isChildOf
    Value: Pamela_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-isChildOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:disjoint :hasBrother,
              :hasSister,
              :isBrotherOf,
              :isSisterOf ;
          sh:path :isChildOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :isChildOf a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:propertyDisjointWith :isSisterOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [14]:
    Severity: Violation
    Focus node: Edwina_Ashley
    Path: hasFather
    Value: Baron_Mount_Temple
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [15]:
    Severity: Violation
    Focus node: Pamela_Hicks
    Path: hasFather
    Value: Louis_Mountbatten
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [16]:
    Severity: Violation
    Focus node: David_Nightingale_Hicks
    Path: hasFather
    Value: Herbert_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [17]:
    Severity: Violation
    Focus node: Louis_Mountbatten
    Path: hasFather
    Value: Prince_Louis_of_Battenberg
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [18]:
    Severity: Violation
    Focus node: Pamela_Hicks
    Path: hasMother
    Value: Edwina_Ashley
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [19]:
    Severity: Violation
    Focus node: David_Nightingale_Hicks
    Path: hasMother
    Value: Iris_Elsie_Platten
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [20]:
    Severity: Violation
    Focus node: Louis_Mountbatten
    Path: hasMother
    Value: Princess_Victoria_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Man']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [21]:
    Severity: Violation
    Focus node: India_Hicks
    Path: isChildOf
    Value: David_Nightingale_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-isChildOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:disjoint :hasBrother,
              :hasSister,
              :isBrotherOf,
              :isSisterOf ;
          sh:path :isChildOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :isChildOf a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:propertyDisjointWith :isSisterOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [22]:
    Severity: Violation
    Focus node: India_Hicks
    Path: isChildOf
    Value: Pamela_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-isChildOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:disjoint :hasBrother,
              :hasSister,
              :isBrotherOf,
              :isSisterOf ;
          sh:path :isChildOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :isChildOf a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:propertyDisjointWith :isSisterOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [23]:
    Severity: Violation
    Focus node: Edwina_Ashley
    Path: hasFather
    Value: Baron_Mount_Temple
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [24]:
    Severity: Violation
    Focus node: Pamela_Hicks
    Path: hasFather
    Value: Louis_Mountbatten
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [25]:
    Severity: Violation
    Focus node: Pamela_Hicks
    Path: hasMother
    Value: Edwina_Ashley
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Person', ':Woman']
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



  Violation [26]:
    Severity: Violation
    Focus node: India_Hicks
    Path: isChildOf
    Value: David_Nightingale_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-isChildOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:disjoint :hasBrother,
              :hasSister,
              :isBrotherOf,
              :isSisterOf ;
          sh:path :isChildOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :isChildOf a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:propertyDisjointWith :isSisterOf .
    Classes assigned to the value node: [':Person', ':Man']
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



  Violation [27]:
    Severity: Violation
    Focus node: India_Hicks
    Path: isChildOf
    Value: Pamela_Hicks
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-isChildOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:disjoint :hasBrother,
              :hasSister,
              :isBrotherOf,
              :isSisterOf ;
          sh:path :isChildOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Person', ':Woman']
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

    Definition of the path:
      :isChildOf a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:propertyDisjointWith :isSisterOf .
    Classes assigned to the value node: [':Person', ':Woman']
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




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The value node Herbert_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Herbert_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Prince_Louis_of_Battenberg is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Prince_Louis_of_Battenberg, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Iris_Elsie_Platten is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Iris_Elsie_Platten, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Princess_Victoria_of_Hesse is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Princess_Victoria_of_Hesse, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Baron_Mount_Temple is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Baron_Mount_Temple, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Louis_Mountbatten is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Louis_Mountbatten, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Herbert_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Herbert_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Prince_Louis_of_Battenberg is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Prince_Louis_of_Battenberg, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Edwina_Ashley is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Edwina_Ashley, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Iris_Elsie_Platten is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Iris_Elsie_Platten, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Princess_Victoria_of_Hesse is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Princess_Victoria_of_Hesse, :Ancestor)"\n    },\n    {\n      "explanation": "The value node David_Nightingale_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(David_Nightingale_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Pamela_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Pamela_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Baron_Mount_Temple is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Baron_Mount_Temple, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Louis_Mountbatten is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Louis_Mountbatten, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Herbert_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Herbert_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Prince_Louis_of_Battenberg is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Prince_Louis_of_Battenberg, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Edwina_Ashley is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Edwina_Ashley, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Iris_Elsie_Platten is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Iris_Elsie_Platten, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Princess_Victoria_of_Hesse is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Princess_Victoria_of_Hesse, :Ancestor)"\n    },\n    {\n      "explanation": "The value node David_Nightingale_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(David_Nightingale_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Pamela_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Pamela_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Baron_Mount_Temple is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Baron_Mount_Temple, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Louis_Mountbatten is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Louis_Mountbatten, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Edwina_Ashley is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Edwina_Ashley, :Ancestor)"\n    },\n    {\n      "explanation": "The value node David_Nightingale_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(David_Nightingale_Hicks, :Ancestor)"\n    },\n    {\n      "explanation": "The value node Pamela_Hicks is missing the required class :Ancestor.",\n      "instruction": "AssignClass(Pamela_Hicks, :Ancestor)"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHtnDnmmwHF+nGoihjdFfEBAJvkIABhkOixlPQ4+2Tx8XSiw+vl77k7k11x7dC'}}]