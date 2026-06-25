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
Total violations:48
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Prince_Georg_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [2]:
    Severity: Violation
    Focus node: Prince_Georg_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [3]:
    Severity: Violation
    Focus node: Prince_Welf_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [4]:
    Severity: Violation
    Focus node: Prince_Welf_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [5]:
    Severity: Violation
    Focus node: Prince_Rainer_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [6]:
    Severity: Violation
    Focus node: Prince_Rainer_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Karl_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Karl_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [9]:
    Severity: Violation
    Focus node: Princess_Christina_of_Hesse
    Path: hasFather
    Value: Prince_Christoph_of_Hesse
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



  Violation [10]:
    Severity: Violation
    Focus node: Princess_Christina_of_Hesse
    Path: hasMother
    Value: Princess_Sophie_of_Greece_and_Denmark
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



  Violation [11]:
    Severity: Violation
    Focus node: Princess_Clarissa_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Princess_Clarissa_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [13]:
    Severity: Violation
    Focus node: Prince_Georg_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [14]:
    Severity: Violation
    Focus node: Prince_Georg_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Princess_Dorothea_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [16]:
    Severity: Violation
    Focus node: Princess_Dorothea_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [17]:
    Severity: Violation
    Focus node: Princess_Friederike_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Princess_Friederike_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [19]:
    Severity: Violation
    Focus node: Prince_Rainer_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Rainer_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Karl_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [22]:
    Severity: Violation
    Focus node: Prince_Karl_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [23]:
    Severity: Violation
    Focus node: Prince_Welf_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Welf_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [25]:
    Severity: Violation
    Focus node: Princess_Christina_of_Hesse
    Path: hasFather
    Value: Prince_Christoph_of_Hesse
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



  Violation [26]:
    Severity: Violation
    Focus node: Princess_Christina_of_Hesse
    Path: hasMother
    Value: Princess_Sophie_of_Greece_and_Denmark
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



  Violation [27]:
    Severity: Violation
    Focus node: Princess_Clarissa_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [28]:
    Severity: Violation
    Focus node: Princess_Clarissa_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [29]:
    Severity: Violation
    Focus node: Prince_Georg_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Georg_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [31]:
    Severity: Violation
    Focus node: Princess_Dorothea_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [32]:
    Severity: Violation
    Focus node: Princess_Dorothea_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Princess_Friederike_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [34]:
    Severity: Violation
    Focus node: Princess_Friederike_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Rainer_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Prince_Rainer_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [37]:
    Severity: Violation
    Focus node: Prince_Karl_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [38]:
    Severity: Violation
    Focus node: Prince_Karl_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [39]:
    Severity: Violation
    Focus node: Prince_Welf_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [40]:
    Severity: Violation
    Focus node: Prince_Welf_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
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
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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



  Violation [41]:
    Severity: Violation
    Focus node: Princess_Christina_of_Hesse
    Path: hasFather
    Value: Prince_Christoph_of_Hesse
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



  Violation [42]:
    Severity: Violation
    Focus node: Princess_Christina_of_Hesse
    Path: hasMother
    Value: Princess_Sophie_of_Greece_and_Denmark
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
    Focus node: Princess_Clarissa_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [44]:
    Severity: Violation
    Focus node: Princess_Clarissa_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Princess_Dorothea_of_Hesse
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [46]:
    Severity: Violation
    Focus node: Princess_Dorothea_of_Hesse
    Path: hasParent
    Value: Prince_Christoph_of_Hesse
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
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
    Focus node: Princess_Friederike_of_Hanover
    Path: hasParent
    Value: Princess_Sophie_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [48]:
    Severity: Violation
    Focus node: Princess_Friederike_of_Hanover
    Path: hasParent
    Value: Prince_George_William_of_Hanover
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasParent a sh:PropertyShape ;
          sh:class :Ancestor,
              :Person ;
          sh:maxCount 2 ;
          sh:path :hasParent .
    SHACL message: Value class is not in classes (:Ancestor, :Person)
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasParent a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Person ;
          rdfs:subPropertyOf :hasAncestor ;
          owl:equivalentProperty :isChildOf ;
          owl:inverseOf :isParentOf .
    Classes assigned to the value node: [':Man']
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

[{'type': 'text', 'text': '{\n  "translations": [\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Man or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Man)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Woman or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Woman)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Man or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Man)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Woman or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Woman)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Man or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Man)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Woman or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Woman)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_Christoph_of_Hesse is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_Christoph_of_Hesse, :Person)"},\n    {"explanation": "The value node Princess_Sophie_of_Greece_and_Denmark is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Princess_Sophie_of_Greece_and_Denmark, :Person)"},\n    {"explanation": "The value node Prince_George_William_of_Hanover is not assigned the required class :Person or :Ancestor.", "instruction": "AssignClass(Prince_George_William_of_Hanover, :Person)"}\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHgX6qs11KOSGkTa7Jf7EjsG/PLgmJbbPoIT9HTv5izlsV5RQz3fU8k4hlQYkQ'}}]