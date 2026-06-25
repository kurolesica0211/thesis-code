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
Total violations:22
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: Grand_Duke_Michael_Nicolaievich_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [3]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Princess_Nina_Georgievna_of_Russia->:hasFather
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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


  Violation [4]:
    Severity: Violation
    Focus node: Princess_Xenia
    Path: hasFather
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [5]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasMother
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [6]:
    Severity: Violation
    Focus node: Princess_Xenia
    Path: hasMother
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [7]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: Grand_Duke_Michael_Nicolaievich_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [8]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [9]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Princess_Nina_Georgievna_of_Russia->:hasFather
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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


  Violation [10]:
    Severity: Violation
    Focus node: Princess_Xenia
    Path: hasFather
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [11]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasMother
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [12]:
    Severity: Violation
    Focus node: Princess_Xenia
    Path: hasMother
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [13]:
    Severity: Violation
    Focus node: Princess_Xenia
    Path: hasFather
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [14]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: Grand_Duke_Michael_Nicolaievich_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [15]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [16]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Princess_Nina_Georgievna_of_Russia->:hasFather
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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


  Violation [17]:
    Severity: Violation
    Focus node: Princess_Xenia
    Path: hasMother
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [18]:
    Severity: Violation
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: hasMother
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
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
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [19]:
    Severity: Violation
    Focus node: Prince_Paul_Chavchavadze
    Path: None
    Value: Prince_Paul_Chavchavadze
    Constraint: ClassConstraintComponent
    Source shape:
      esh:DomainConjunctionShape_isFatherOf a sh:NodeShape ;
          sh:class :Ancestor,
              :Man ;
          sh:message "Any subject of isFatherOf must be all of: Ancestor, Man." ;
          sh:targetSubjectsOf :isFatherOf .
    SHACL message: Any subject of isFatherOf must be all of: Ancestor, Man.
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
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
    Focus node: Grand_Duke_George_Mikhailovich
    Path: None
    Value: Grand_Duke_George_Mikhailovich
    Constraint: ClassConstraintComponent
    Source shape:
      esh:DomainConjunctionShape_isFatherOf a sh:NodeShape ;
          sh:class :Ancestor,
              :Man ;
          sh:message "Any subject of isFatherOf must be all of: Ancestor, Man." ;
          sh:targetSubjectsOf :isFatherOf .
    SHACL message: Any subject of isFatherOf must be all of: Ancestor, Man.
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
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
    Focus node: Princess_Nina_Georgievna_of_Russia
    Path: None
    Value: Princess_Nina_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      esh:DomainConjunctionShape_isMotherOf a sh:NodeShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:message "Any subject of isMotherOf must be all of: Ancestor, Woman." ;
          sh:targetSubjectsOf :isMotherOf .
    SHACL message: Any subject of isMotherOf must be all of: Ancestor, Woman.
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [22]:
    Severity: Violation
    Focus node: Grand_Duchess_Maria_Georgievna_of_Russia
    Path: None
    Value: Grand_Duchess_Maria_Georgievna_of_Russia
    Constraint: ClassConstraintComponent
    Source shape:
      esh:DomainConjunctionShape_isMotherOf a sh:NodeShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:message "Any subject of isMotherOf must be all of: Ancestor, Woman." ;
          sh:targetSubjectsOf :isMotherOf .
    SHACL message: Any subject of isMotherOf must be all of: Ancestor, Woman.
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasFather relationship with Grand_Duke_Michael_Nicolaievich_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_Michael_Nicolaievich_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasFather relationship with Grand_Duke_George_Mikhailovich, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has more than one hasFather relationship, which violates the functional property constraint (maxCount 1).",\n      "instruction": "RemoveTriple(subject=\'Princess_Nina_Georgievna_of_Russia\', predicate=\':hasFather\', object=\'Grand_Duke_Michael_Nicolaievich_of_Russia\')"\n    },\n    {\n      "explanation": "The node Princess_Xenia has a hasFather relationship with Grand_Duke_George_Mikhailovich, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasMother relationship with Grand_Duchess_Maria_Georgievna_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Xenia has a hasMother relationship with Grand_Duchess_Maria_Georgievna_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasFather relationship with Grand_Duke_Michael_Nicolaievich_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_Michael_Nicolaievich_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasFather relationship with Grand_Duke_George_Mikhailovich, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has more than one hasFather relationship, which violates the functional property constraint (maxCount 1).",\n      "instruction": "RemoveTriple(subject=\'Princess_Nina_Georgievna_of_Russia\', predicate=\':hasFather\', object=\'Grand_Duke_George_Mikhailovich\')"\n    },\n    {\n      "explanation": "The node Princess_Xenia has a hasFather relationship with Grand_Duke_George_Mikhailovich, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasMother relationship with Grand_Duchess_Maria_Georgievna_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Xenia has a hasMother relationship with Grand_Duchess_Maria_Georgievna_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Xenia has a hasFather relationship with Grand_Duke_George_Mikhailovich, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasFather relationship with Grand_Duke_Michael_Nicolaievich_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_Michael_Nicolaievich_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasFather relationship with Grand_Duke_George_Mikhailovich, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has more than one hasFather relationship, which violates the functional property constraint (maxCount 1).",\n      "instruction": "RemoveTriple(subject=\'Princess_Nina_Georgievna_of_Russia\', predicate=\':hasFather\', object=\'Grand_Duke_Michael_Nicolaievich_of_Russia\')"\n    },\n    {\n      "explanation": "The node Princess_Xenia has a hasMother relationship with Grand_Duchess_Maria_Georgievna_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia has a hasMother relationship with Grand_Duchess_Maria_Georgievna_of_Russia, but the target node is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Prince_Paul_Chavchavadze is the subject of an isFatherOf relation, but it is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Prince_Paul_Chavchavadze\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Grand_Duke_George_Mikhailovich is the subject of an isFatherOf relation, but it is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duke_George_Mikhailovich\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Nina_Georgievna_of_Russia is the subject of an isMotherOf relation, but it is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Princess_Nina_Georgievna_of_Russia\', class=\':Ancestor\')"\n    },\n    {\n      "explanation": "The node Grand_Duchess_Maria_Georgievna_of_Russia is the subject of an isMotherOf relation, but it is missing the mandatory class :Ancestor.",\n      "instruction": "AssignClass(node=\'Grand_Duchess_Maria_Georgievna_of_Russia\', class=\':Ancestor\')"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHbvqpPKfS+IwSNND3JdUi1ehG7ofmHLx0U+YV+pQnWsrtJKDHsWjhjE5GcRFt'}}]