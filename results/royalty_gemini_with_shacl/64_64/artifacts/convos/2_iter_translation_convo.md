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
Total violations:20
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: isSonOf
    Value: KingGeorgeIOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-isSonOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isSonOf .
    SHACL message: Value does not have class :Ancestor
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

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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



  Violation [2]:
    Severity: Violation
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: isSonOf
    Value: QueenOlgaOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-isSonOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isSonOf .
    SHACL message: Value does not have class :Ancestor
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

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: hasFather
    Value: KingGeorgeIOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: hasMother
    Value: QueenOlgaOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: isSonOf
    Value: KingGeorgeIOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-isSonOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isSonOf .
    SHACL message: Value does not have class :Ancestor
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

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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



  Violation [6]:
    Severity: Violation
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: isSonOf
    Value: QueenOlgaOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-isSonOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isSonOf .
    SHACL message: Value does not have class :Ancestor
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

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [7]:
    Severity: Violation
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: hasFather
    Value: KingGeorgeIOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: hasMother
    Value: QueenOlgaOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: isSonOf
    Value: KingGeorgeIOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-isSonOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isSonOf .
    SHACL message: Value does not have class :Ancestor
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

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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



  Violation [10]:
    Severity: Violation
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: isSonOf
    Value: QueenOlgaOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Man-isSonOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isSonOf .
    SHACL message: Value does not have class :Ancestor
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

    Definition of the path:
      :isSonOf a owl:ObjectProperty ;
          rdfs:domain :Man ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: hasFather
    Value: KingGeorgeIOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
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
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: hasMother
    Value: QueenOlgaOfGreece
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
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
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [13]:
    Severity: Violation
    Focus node: KingGeorgeIOfGreece
    Path: None
    Value: KingGeorgeIOfGreece
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



  Violation [14]:
    Severity: Violation
    Focus node: PrinceAndrewOfGreeceAndDenmark
    Path: None
    Value: PrinceAndrewOfGreeceAndDenmark
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



  Violation [15]:
    Severity: Violation
    Focus node: ConstantineOfGreece
    Path: None
    Value: ConstantineOfGreece
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



  Violation [16]:
    Severity: Violation
    Focus node: KingChristianIXOfDenmark
    Path: None
    Value: KingChristianIXOfDenmark
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



  Violation [17]:
    Severity: Violation
    Focus node: PrinceLouisOfBattenberg
    Path: None
    Value: PrinceLouisOfBattenberg
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



  Violation [18]:
    Severity: Violation
    Focus node: PrincessVictoriaOfHesseAndByRhine
    Path: None
    Value: PrincessVictoriaOfHesseAndByRhine
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



  Violation [19]:
    Severity: Violation
    Focus node: PrincessAliceOfBattenberg
    Path: None
    Value: PrincessAliceOfBattenberg
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



  Violation [20]:
    Severity: Violation
    Focus node: QueenOlgaOfGreece
    Path: None
    Value: QueenOlgaOfGreece
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

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node KingGeorgeIOfGreece is used as an :isSonOf value, but it lacks the required :Ancestor class.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece is used as an :isSonOf value, but it lacks the required :Ancestor class.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingGeorgeIOfGreece is assigned as a father, but it lacks the mandatory :Ancestor class.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece is assigned as a mother, but it lacks the mandatory :Ancestor class.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingGeorgeIOfGreece is missing the required :Ancestor class for the :isSonOf property.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece is missing the required :Ancestor class for the :isSonOf property.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingGeorgeIOfGreece is missing the required :Ancestor class for the :hasFather property.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece is missing the required :Ancestor class for the :hasMother property.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingGeorgeIOfGreece is missing the required :Ancestor class for the :isSonOf property.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece is missing the required :Ancestor class for the :isSonOf property.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingGeorgeIOfGreece is missing the required :Ancestor class for the :hasFather property.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece is missing the required :Ancestor class for the :hasMother property.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingGeorgeIOfGreece acts as a subject for :isFatherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'KingGeorgeIOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node PrinceAndrewOfGreeceAndDenmark acts as a subject for :isFatherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'PrinceAndrewOfGreeceAndDenmark\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node ConstantineOfGreece acts as a subject for :isFatherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'ConstantineOfGreece\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node KingChristianIXOfDenmark acts as a subject for :isFatherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'KingChristianIXOfDenmark\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node PrinceLouisOfBattenberg acts as a subject for :isFatherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'PrinceLouisOfBattenberg\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node PrincessVictoriaOfHesseAndByRhine acts as a subject for :isMotherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'PrincessVictoriaOfHesseAndByRhine\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node PrincessAliceOfBattenberg acts as a subject for :isMotherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'PrincessAliceOfBattenberg\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node QueenOlgaOfGreece acts as a subject for :isMotherOf but is missing the :Ancestor class.",\n      "instruction": "AssignClass(node: \'QueenOlgaOfGreece\', class: \':Ancestor\')"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbH4oz6OcdFyaw0Slkm21ce7RJU4QQ59RHhojAeIP4AwHPimp6didIf+ZUyKo9M'}}]