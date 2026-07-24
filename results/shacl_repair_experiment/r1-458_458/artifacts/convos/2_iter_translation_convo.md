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
Total violations:75
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Pavlos
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



  Violation [2]:
    Severity: Violation
    Focus node: Carlos_Javier_Morales_Quintana
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



  Violation [3]:
    Severity: Violation
    Focus node: Constantine_II
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



  Violation [4]:
    Severity: Violation
    Focus node: Kyril
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



  Violation [5]:
    Severity: Violation
    Focus node: Simeon_of_Bulgaria
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



  Violation [6]:
    Severity: Violation
    Focus node: Pavlos
    Path: hasFather
    Value: Constantine_II
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



  Violation [7]:
    Severity: Violation
    Focus node: Kyril
    Path: hasFather
    Value: Simeon_of_Bulgaria
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
    Focus node: Pavlos
    Path: hasMother
    Value: Anne-Marie
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
    Focus node: Pavlos
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [10]:
    Severity: Violation
    Focus node: Carlos_Javier_Morales_Quintana
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [11]:
    Severity: Violation
    Focus node: Constantine_II
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [12]:
    Severity: Violation
    Focus node: Kyril
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [13]:
    Severity: Violation
    Focus node: Simeon_of_Bulgaria
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [14]:
    Severity: Violation
    Focus node: Alexia
    Path: hasFather
    Value: Constantine_II
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
    Focus node: Pavlos
    Path: hasFather
    Value: Constantine_II
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



  Violation [16]:
    Severity: Violation
    Focus node: Kyril
    Path: hasFather
    Value: Simeon_of_Bulgaria
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
    Focus node: Theodora
    Path: hasFather
    Value: Constantine_II
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
    Focus node: Alexia
    Path: hasMother
    Value: Anne-Marie
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
    Focus node: Pavlos
    Path: hasMother
    Value: Anne-Marie
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



  Violation [20]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasMother
    Value: Kyril
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
    Focus node: Mafalda
    Path: hasMother
    Value: Kyril
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
    Focus node: Theodora
    Path: hasMother
    Value: Anne-Marie
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



  Violation [23]:
    Severity: Violation
    Focus node: Maria-Olympia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [24]:
    Severity: Violation
    Focus node: Alexia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [25]:
    Severity: Violation
    Focus node: Pavlos
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [26]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [27]:
    Severity: Violation
    Focus node: Ingrid
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [28]:
    Severity: Violation
    Focus node: Anne-Marie
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [29]:
    Severity: Violation
    Focus node: Kyril
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [30]:
    Severity: Violation
    Focus node: Theodora
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [31]:
    Severity: Violation
    Focus node: Carlos_Javier_Morales_Quintana
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [32]:
    Severity: Violation
    Focus node: Sofia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [33]:
    Severity: Violation
    Focus node: Constantine_II
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [34]:
    Severity: Violation
    Focus node: Simeon_of_Bulgaria
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [35]:
    Severity: Violation
    Focus node: Alexia
    Path: hasFather
    Value: Constantine_II
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



  Violation [36]:
    Severity: Violation
    Focus node: Theodora
    Path: hasFather
    Value: Constantine_II
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



  Violation [37]:
    Severity: Violation
    Focus node: Alexia
    Path: hasMother
    Value: Anne-Marie
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



  Violation [38]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasMother
    Value: Kyril
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
    Focus node: Mafalda
    Path: hasMother
    Value: Kyril
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [40]:
    Severity: Violation
    Focus node: Theodora
    Path: hasMother
    Value: Anne-Marie
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



  Violation [41]:
    Severity: Violation
    Focus node: Maria-Olympia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [42]:
    Severity: Violation
    Focus node: Alexia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [43]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [44]:
    Severity: Violation
    Focus node: Sofia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [45]:
    Severity: Violation
    Focus node: Ingrid
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [46]:
    Severity: Violation
    Focus node: Anne-Marie
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [47]:
    Severity: Violation
    Focus node: Theodora
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [48]:
    Severity: Violation
    Focus node: Maria-Olympia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [49]:
    Severity: Violation
    Focus node: Alexia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [50]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [51]:
    Severity: Violation
    Focus node: Sofia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [52]:
    Severity: Violation
    Focus node: Ingrid
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [53]:
    Severity: Violation
    Focus node: Anne-Marie
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [54]:
    Severity: Violation
    Focus node: Theodora
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-hasSex a sh:PropertyShape ;
          dash:hasValueWithClass :Female ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [55]:
    Severity: Violation
    Focus node: Alexia
    Path: hasFather
    Value: Constantine_II
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



  Violation [56]:
    Severity: Violation
    Focus node: Pavlos
    Path: hasFather
    Value: Constantine_II
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



  Violation [57]:
    Severity: Violation
    Focus node: Kyril
    Path: hasFather
    Value: Simeon_of_Bulgaria
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



  Violation [58]:
    Severity: Violation
    Focus node: Theodora
    Path: hasFather
    Value: Constantine_II
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



  Violation [59]:
    Severity: Violation
    Focus node: Alexia
    Path: hasMother
    Value: Anne-Marie
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



  Violation [60]:
    Severity: Violation
    Focus node: Pavlos
    Path: hasMother
    Value: Anne-Marie
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



  Violation [61]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasMother
    Value: Kyril
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [62]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasMother
    Value: Kyril
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
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [63]:
    Severity: Violation
    Focus node: Theodora
    Path: hasMother
    Value: Anne-Marie
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



  Violation [64]:
    Severity: Violation
    Focus node: Maria-Olympia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [65]:
    Severity: Violation
    Focus node: Alexia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [66]:
    Severity: Violation
    Focus node: Pavlos
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [67]:
    Severity: Violation
    Focus node: Mafalda
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [68]:
    Severity: Violation
    Focus node: Ingrid
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [69]:
    Severity: Violation
    Focus node: Anne-Marie
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [70]:
    Severity: Violation
    Focus node: Kyril
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [71]:
    Severity: Violation
    Focus node: Theodora
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [72]:
    Severity: Violation
    Focus node: Carlos_Javier_Morales_Quintana
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [73]:
    Severity: Violation
    Focus node: Sofia
    Path: hasSex
    Value: Female
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSex a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Sex .
    Classes assigned to the value node: []
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [74]:
    Severity: Violation
    Focus node: Constantine_II
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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



  Violation [75]:
    Severity: Violation
    Focus node: Simeon_of_Bulgaria
    Path: hasSex
    Value: Male
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSex a sh:PropertyShape ;
          sh:class :Sex ;
          sh:maxCount 1 ;
          sh:path :hasSex .
    SHACL message: Value does not have class :Sex
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




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Pavlos\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Carlos_Javier_Morales_Quintana\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Constantine_II\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Kyril\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Simeon_of_Bulgaria\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Pavlos\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Simeon_of_Bulgaria\' assigned to \'hasFather\' for \'Kyril\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Simeon_of_Bulgaria\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Pavlos\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Pavlos\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Carlos_Javier_Morales_Quintana\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Constantine_II\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Kyril\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Simeon_of_Bulgaria\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Alexia\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Pavlos\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Simeon_of_Bulgaria\' assigned to \'hasFather\' for \'Kyril\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Simeon_of_Bulgaria\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Theodora\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Alexia\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Pavlos\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Kyril\' assigned to \'hasMother\' for \'Mafalda\' lacks the necessary \':Ancestor\' and \':Woman\' classes.", "instruction": "AssignClass(node=\'Kyril\', class=\':Ancestor\'); AssignClass(node=\'Kyril\', class=\':Woman\')"},\n    {"explanation": "The node \'Kyril\' assigned to \'hasMother\' for \'Mafalda\' lacks the necessary \':Ancestor\' and \':Woman\' classes.", "instruction": "AssignClass(node=\'Kyril\', class=\':Ancestor\'); AssignClass(node=\'Kyril\', class=\':Woman\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Theodora\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Maria-Olympia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Alexia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Pavlos\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Mafalda\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Ingrid\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Anne-Marie\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Kyril\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Theodora\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Carlos_Javier_Morales_Quintana\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Sofia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Constantine_II\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Simeon_of_Bulgaria\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Alexia\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Theodora\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Alexia\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Kyril\' assigned to \'hasMother\' for \'Mafalda\' lacks the necessary \':Ancestor\' and \':Woman\' classes.", "instruction": "AssignClass(node=\'Kyril\', class=\':Ancestor\'); AssignClass(node=\'Kyril\', class=\':Woman\')"},\n    {"explanation": "The node \'Kyril\' assigned to \'hasMother\' for \'Mafalda\' lacks the necessary \':Ancestor\' and \':Woman\' classes.", "instruction": "AssignClass(node=\'Kyril\', class=\':Ancestor\'); AssignClass(node=\'Kyril\', class=\':Woman\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Theodora\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Maria-Olympia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Alexia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Mafalda\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Sofia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Ingrid\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Anne-Marie\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Theodora\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Maria-Olympia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Alexia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Mafalda\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Sofia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Ingrid\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Anne-Marie\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Theodora\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Alexia\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Pavlos\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Simeon_of_Bulgaria\' assigned to \'hasFather\' for \'Kyril\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Simeon_of_Bulgaria\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Constantine_II\' assigned to \'hasFather\' for \'Theodora\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Constantine_II\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Alexia\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Pavlos\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The node \'Kyril\' assigned to \'hasMother\' for \'Mafalda\' lacks the necessary \':Ancestor\' and \':Woman\' classes.", "instruction": "AssignClass(node=\'Kyril\', class=\':Ancestor\'); AssignClass(node=\'Kyril\', class=\':Woman\')"},\n    {"explanation": "The node \'Kyril\' assigned to \'hasMother\' for \'Mafalda\' lacks the necessary \':Ancestor\' and \':Woman\' classes.", "instruction": "AssignClass(node=\'Kyril\', class=\':Ancestor\'); AssignClass(node=\'Kyril\', class=\':Woman\')"},\n    {"explanation": "The node \'Anne-Marie\' assigned to \'hasMother\' for \'Theodora\' lacks the necessary \':Ancestor\' class.", "instruction": "AssignClass(node=\'Anne-Marie\', class=\':Ancestor\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Maria-Olympia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Alexia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Pavlos\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Mafalda\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Ingrid\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Anne-Marie\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Kyril\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Theodora\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Carlos_Javier_Morales_Quintana\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Female\' for the property \'hasSex\' on the node \'Sofia\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Female\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Constantine_II\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"},\n    {"explanation": "The value \'Male\' for the property \'hasSex\' on the node \'Simeon_of_Bulgaria\' is missing the required class \':Sex\'.", "instruction": "AssignClass(node=\'Male\', class=\':Sex\')"}\n  ]\n}', 'extras': {'signature': 'EjQKMgERTTIPU/cbamH2zABL4cme/05YPr5iYastekEfTklO1l6+fNsG9C+szmrgeVq4xIj6'}}]