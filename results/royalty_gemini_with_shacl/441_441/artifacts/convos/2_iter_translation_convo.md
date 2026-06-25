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
Total violations:51
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: John_Herbert_Bowes-Lyon
    Path: hasFather
    Value: Claude_Bowes-Lyon
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



  Violation [2]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Jane_McDonnell
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Jane_McDonnell
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Charles_Hepburn-Stuart-Forbes-Trefusis_21st->:hasFather
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


  Violation [6]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [8]:
    Severity: Violation
    Focus node: John_Herbert_Bowes-Lyon
    Path: hasMother
    Value: Cecilia_Bowes-Lyon
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasMother
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [10]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Jane_McDonnell
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Jane_McDonnell
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
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Charles_Hepburn-Stuart-Forbes-Trefusis_21st->:hasFather
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


  Violation [14]:
    Severity: Violation
    Focus node: Katherine_Bowes-Lyon
    Path: hasFather
    Value: John_Herbert_Bowes-Lyon
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
    Focus node: Nerissa_Bowes-Lyon
    Path: hasFather
    Value: John_Herbert_Bowes-Lyon
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
    Focus node: John_Herbert_Bowes-Lyon
    Path: hasFather
    Value: Claude_Bowes-Lyon
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



  Violation [17]:
    Severity: Violation
    Focus node: Fenella_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
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



  Violation [18]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [19]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [20]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
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



  Violation [21]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Henry_Nevile_Fane
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



  Violation [22]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Harriet_Hepburn-Stuart-Forbes-Trefusis->:hasFather
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


  Violation [23]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasMother
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [24]:
    Severity: Violation
    Focus node: Katherine_Bowes-Lyon
    Path: hasMother
    Value: Fenella_Hepburn-Stuart-Forbes-Trefusis
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



  Violation [25]:
    Severity: Violation
    Focus node: Nerissa_Bowes-Lyon
    Path: hasMother
    Value: Fenella_Hepburn-Stuart-Forbes-Trefusis
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



  Violation [26]:
    Severity: Violation
    Focus node: John_Herbert_Bowes-Lyon
    Path: hasMother
    Value: Cecilia_Bowes-Lyon
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



  Violation [27]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Jane_McDonnell
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



  Violation [28]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
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



  Violation [29]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: Jane_McDonnell
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



  Violation [30]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Charles_Hepburn-Stuart-Forbes-Trefusis_21st->:hasFather
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


  Violation [31]:
    Severity: Violation
    Focus node: Katherine_Bowes-Lyon
    Path: hasFather
    Value: John_Herbert_Bowes-Lyon
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



  Violation [32]:
    Severity: Violation
    Focus node: Nerissa_Bowes-Lyon
    Path: hasFather
    Value: John_Herbert_Bowes-Lyon
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



  Violation [33]:
    Severity: Violation
    Focus node: John_Herbert_Bowes-Lyon
    Path: hasFather
    Value: Claude_Bowes-Lyon
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



  Violation [34]:
    Severity: Violation
    Focus node: Fenella_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
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



  Violation [35]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [36]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_20th
    Path: hasFather
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [37]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
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



  Violation [38]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Henry_Nevile_Fane
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



  Violation [39]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Harriet_Hepburn-Stuart-Forbes-Trefusis->:hasFather
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


  Violation [40]:
    Severity: Violation
    Focus node: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
    Path: hasMother
    Value: Harriet_Williamina_Hepburn-Forbes
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



  Violation [41]:
    Severity: Violation
    Focus node: Katherine_Bowes-Lyon
    Path: hasMother
    Value: Fenella_Hepburn-Stuart-Forbes-Trefusis
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



  Violation [42]:
    Severity: Violation
    Focus node: Nerissa_Bowes-Lyon
    Path: hasMother
    Value: Fenella_Hepburn-Stuart-Forbes-Trefusis
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



  Violation [43]:
    Severity: Violation
    Focus node: John_Herbert_Bowes-Lyon
    Path: hasMother
    Value: Cecilia_Bowes-Lyon
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



  Violation [44]:
    Severity: Violation
    Focus node: Katherine_Bowes-Lyon
    Path: hasFather
    Value: John_Herbert_Bowes-Lyon
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



  Violation [45]:
    Severity: Violation
    Focus node: Nerissa_Bowes-Lyon
    Path: hasFather
    Value: John_Herbert_Bowes-Lyon
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



  Violation [46]:
    Severity: Violation
    Focus node: Fenella_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
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



  Violation [47]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Charles_Hepburn-Stuart-Forbes-Trefusis_21st
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



  Violation [48]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: Henry_Nevile_Fane
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



  Violation [49]:
    Severity: Violation
    Focus node: Harriet_Hepburn-Stuart-Forbes-Trefusis
    Path: hasFather
    Value: None
    Constraint: MaxCountConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: More than 1 values on data:Harriet_Hepburn-Stuart-Forbes-Trefusis->:hasFather
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


  Violation [50]:
    Severity: Violation
    Focus node: Katherine_Bowes-Lyon
    Path: hasMother
    Value: Fenella_Hepburn-Stuart-Forbes-Trefusis
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



  Violation [51]:
    Severity: Violation
    Focus node: Nerissa_Bowes-Lyon
    Path: hasMother
    Value: Fenella_Hepburn-Stuart-Forbes-Trefusis
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




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {"explanation": "The person Claude_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Claude_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Jane_McDonnell is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Jane_McDonnell, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_20th is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_20th, :Ancestor)"},\n    {"explanation": "The person Jane_McDonnell is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Jane_McDonnell, :Ancestor)"},\n    {"explanation": "The node Charles_Hepburn-Stuart-Forbes-Trefusis_21st has more than one father defined, but the property is functional and only allows one.", "instruction": "RemoveTriple(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :hasFather, [value])"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Cecilia_Bowes-Lyon is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Cecilia_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Jane_McDonnell is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Jane_McDonnell, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_20th is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_20th, :Ancestor)"},\n    {"explanation": "The person Jane_McDonnell is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Jane_McDonnell, :Ancestor)"},\n    {"explanation": "The node Charles_Hepburn-Stuart-Forbes-Trefusis_21st has more than one father defined, but the property is functional and only allows one.", "instruction": "RemoveTriple(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :hasFather, [value])"},\n    {"explanation": "The person John_Herbert_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(John_Herbert_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person John_Herbert_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(John_Herbert_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Claude_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Claude_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_21st is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :Ancestor)"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_21st is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :Ancestor)"},\n    {"explanation": "The person Henry_Nevile_Fane is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Henry_Nevile_Fane, :Ancestor)"},\n    {"explanation": "The node Harriet_Hepburn-Stuart-Forbes-Trefusis has more than one father defined, but the property is functional and only allows one.", "instruction": "RemoveTriple(Harriet_Hepburn-Stuart-Forbes-Trefusis, :hasFather, [value])"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Fenella_Hepburn-Stuart-Forbes-Trefusis is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Fenella_Hepburn-Stuart-Forbes-Trefusis, :Ancestor)"},\n    {"explanation": "The person Fenella_Hepburn-Stuart-Forbes-Trefusis is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Fenella_Hepburn-Stuart-Forbes-Trefusis, :Ancestor)"},\n    {"explanation": "The person Cecilia_Bowes-Lyon is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Cecilia_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Jane_McDonnell is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Jane_McDonnell, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_20th is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_20th, :Ancestor)"},\n    {"explanation": "The person Jane_McDonnell is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Jane_McDonnell, :Ancestor)"},\n    {"explanation": "The node Charles_Hepburn-Stuart-Forbes-Trefusis_21st has more than one father defined, but the property is functional and only allows one.", "instruction": "RemoveTriple(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :hasFather, [value])"},\n    {"explanation": "The person John_Herbert_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(John_Herbert_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person John_Herbert_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(John_Herbert_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Claude_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Claude_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_21st is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :Ancestor)"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_21st is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :Ancestor)"},\n    {"explanation": "The person Henry_Nevile_Fane is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Henry_Nevile_Fane, :Ancestor)"},\n    {"explanation": "The node Harriet_Hepburn-Stuart-Forbes-Trefusis has more than one father defined, but the property is functional and only allows one.", "instruction": "RemoveTriple(Harriet_Hepburn-Stuart-Forbes-Trefusis, :hasFather, [value])"},\n    {"explanation": "The person Harriet_Williamina_Hepburn-Forbes is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Harriet_Williamina_Hepburn-Forbes, :Ancestor)"},\n    {"explanation": "The person Fenella_Hepburn-Stuart-Forbes-Trefusis is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Fenella_Hepburn-Stuart-Forbes-Trefusis, :Ancestor)"},\n    {"explanation": "The person Fenella_Hepburn-Stuart-Forbes-Trefusis is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Fenella_Hepburn-Stuart-Forbes-Trefusis, :Ancestor)"},\n    {"explanation": "The person Cecilia_Bowes-Lyon is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Cecilia_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person John_Herbert_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(John_Herbert_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person John_Herbert_Bowes-Lyon is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(John_Herbert_Bowes-Lyon, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_21st is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :Ancestor)"},\n    {"explanation": "The person Charles_Hepburn-Stuart-Forbes-Trefusis_21st is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Charles_Hepburn-Stuart-Forbes-Trefusis_21st, :Ancestor)"},\n    {"explanation": "The person Henry_Nevile_Fane is not classified as an Ancestor, which is required for the hasFather property.", "instruction": "AssignClass(Henry_Nevile_Fane, :Ancestor)"},\n    {"explanation": "The node Harriet_Hepburn-Stuart-Forbes-Trefusis has more than one father defined, but the property is functional and only allows one.", "instruction": "RemoveTriple(Harriet_Hepburn-Stuart-Forbes-Trefusis, :hasFather, [value])"},\n    {"explanation": "The person Fenella_Hepburn-Stuart-Forbes-Trefusis is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Fenella_Hepburn-Stuart-Forbes-Trefusis, :Ancestor)"},\n    {"explanation": "The person Fenella_Hepburn-Stuart-Forbes-Trefusis is not classified as an Ancestor, which is required for the hasMother property.", "instruction": "AssignClass(Fenella_Hepburn-Stuart-Forbes-Trefusis, :Ancestor)"}\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHK/y/rOzFKcVyU4NlzofcEAJWb7qYMbi1ni0cLX1w+cHWqF+0RKNAkKWCzd0n'}}]