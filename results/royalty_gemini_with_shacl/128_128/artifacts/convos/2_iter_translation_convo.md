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
Total violations:6
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Princess_Carolina_of_Bourbon-Parma
    Path: isDaughterOf
    Value: Princess_Irene_of_the_Netherlands
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-isDaughterOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isDaughterOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :isDaughterOf a owl:ObjectProperty ;
          rdfs:domain :Woman ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: Princess_Carolina_of_Bourbon-Parma
    Path: isDaughterOf
    Value: Carlos_Hugo_Duke_of_Parma
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-isDaughterOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isDaughterOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :isDaughterOf a owl:ObjectProperty ;
          rdfs:domain :Woman ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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
    Focus node: Princess_Carolina_of_Bourbon-Parma
    Path: isDaughterOf
    Value: Princess_Irene_of_the_Netherlands
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-isDaughterOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isDaughterOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :isDaughterOf a owl:ObjectProperty ;
          rdfs:domain :Woman ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [4]:
    Severity: Violation
    Focus node: Princess_Carolina_of_Bourbon-Parma
    Path: isDaughterOf
    Value: Carlos_Hugo_Duke_of_Parma
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-isDaughterOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isDaughterOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :isDaughterOf a owl:ObjectProperty ;
          rdfs:domain :Woman ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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
    Focus node: Princess_Carolina_of_Bourbon-Parma
    Path: isDaughterOf
    Value: Princess_Irene_of_the_Netherlands
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-isDaughterOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isDaughterOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :isDaughterOf a owl:ObjectProperty ;
          rdfs:domain :Woman ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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
    Focus node: Princess_Carolina_of_Bourbon-Parma
    Path: isDaughterOf
    Value: Carlos_Hugo_Duke_of_Parma
    Constraint: ClassConstraintComponent
    Source shape:
      :Woman-isDaughterOf a sh:PropertyShape ;
          sh:class :Ancestor ;
          sh:path :isDaughterOf .
    SHACL message: Value does not have class :Ancestor
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :isDaughterOf a owl:ObjectProperty ;
          rdfs:domain :Woman ;
          rdfs:range :Ancestor ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf .
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

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Princess_Irene_of_the_Netherlands is referenced as an ancestor for Princess_Carolina_of_Bourbon-Parma via the isDaughterOf property, but it lacks the mandatory :Ancestor class.",\n      "instruction": "AssignClass(node: \'Princess_Irene_of_the_Netherlands\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node Carlos_Hugo_Duke_of_Parma is referenced as an ancestor for Princess_Carolina_of_Bourbon-Parma via the isDaughterOf property, but it lacks the mandatory :Ancestor class.",\n      "instruction": "AssignClass(node: \'Carlos_Hugo_Duke_of_Parma\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Irene_of_the_Netherlands is missing the :Ancestor class, which is required by the :isDaughterOf property definition.",\n      "instruction": "AssignClass(node: \'Princess_Irene_of_the_Netherlands\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node Carlos_Hugo_Duke_of_Parma is missing the :Ancestor class, which is required by the :isDaughterOf property definition.",\n      "instruction": "AssignClass(node: \'Carlos_Hugo_Duke_of_Parma\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node Princess_Irene_of_the_Netherlands is missing the :Ancestor class, which is required by the :isDaughterOf property definition.",\n      "instruction": "AssignClass(node: \'Princess_Irene_of_the_Netherlands\', class: \':Ancestor\')"\n    },\n    {\n      "explanation": "The node Carlos_Hugo_Duke_of_Parma is missing the :Ancestor class, which is required by the :isDaughterOf property definition.",\n      "instruction": "AssignClass(node: \'Carlos_Hugo_Duke_of_Parma\', class: \':Ancestor\')"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgEMOdbHAXX8GbV8VlGk8cu0W578boobZcBvVTT/jO8fN4FdX28fLAJwej9N2dgDQC9J'}}]