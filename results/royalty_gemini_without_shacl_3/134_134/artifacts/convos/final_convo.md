================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin (German: Friedrich Franz Erbgroßherzog von Mecklenburg-Schwerin; 22 April 1910 – 31 July 2001) was the heir apparent to the throne of Mecklenburg-Schwerin and a member of the Waffen-SS.
Early life

He was born in Schwerin, the eldest child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife Princess Alexandra of Hanover, a daughter of Crown Prince Ernest Augustus of Hanover (a first-cousin once removed of Queen Victoria) and Princess Thyra of Denmark, the youngest daughter of King Christian IX of Denmark.
He did not succeed to the throne, as the Grand Duchy was replaced with the Free State of Mecklenburg-Schwerin.
Upon the promulgation of the Weimar Constitution on 11 August 1919, titles of sovereigns such as emperor/empress, king/queen, grand duke/grand duchess, etc. were abolished.
He therefore became known as Friedrich Franz Herzog von Mecklenburg-Schwerin (or Friedrich Franz, Duke of Mecklenburg-Schwerin) de facto since the establishment of the Free State of Mecklenburg-Schwerin.
Post monarchy

In May 1931 against the will of his father, Friedrich Franz joined the SS and by 1936 he had been promoted to the rank of Hauptsturmführer (Captain).
In May 1943, a family council was called by the Grand Ducal family and Friedrich Franz was passed over as heir (of the family estates) in favour of his younger brother Duke Christian Louis, who would instead inherit the family property.
Friedrich Franz married Karin Elisabeth von Schaper (1920–2012), the daughter of Walter von Schaper and his wife Baroness Louise von Münchhausen, on 11 June 1941 at Schloß Wiligrad, near the Lake Schwerin.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (aed8c6b5-a865-458d-ab20-c2c8d4afd189)
 Call ID: aed8c6b5-a865-458d-ab20-c2c8d4afd189
  Args:
    source: Friedrich_Franz
    type: :Man
  AssignClass (af2cd7c8-9cdf-4204-8b00-e74536d15bb3)
 Call ID: af2cd7c8-9cdf-4204-8b00-e74536d15bb3
  Args:
    source: Friedrich_Franz
    type: :Person
  AddLiteral (9358575c-a880-43b9-82a8-7b35c21e2623)
 Call ID: 9358575c-a880-43b9-82a8-7b35c21e2623
  Args:
    relation: :hasBirthYear
    literal_value: 1910
    literal_type: xsd:integer
    source: Friedrich_Franz
  AddLiteral (0ccc76d7-f9dc-4c12-9085-df707638a54a)
 Call ID: 0ccc76d7-f9dc-4c12-9085-df707638a54a
  Args:
    relation: :hasDeathYear
    source: Friedrich_Franz
    literal_type: xsd:integer
    literal_value: 2001
  AssignClass (ebe06385-8d38-433e-b903-4782574b1b54)
 Call ID: ebe06385-8d38-433e-b903-4782574b1b54
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (a5aa2941-3246-4ccc-b577-cc8956f69657)
 Call ID: a5aa2941-3246-4ccc-b577-cc8956f69657
  Args:
    source: Frederick_Francis_IV
    type: :Person
  AssignClass (9e4aeb30-8343-4619-ba7e-820ed36c5e00)
 Call ID: 9e4aeb30-8343-4619-ba7e-820ed36c5e00
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Hanover
  AssignClass (788f737a-1bc6-40fe-8bce-c140ff601501)
 Call ID: 788f737a-1bc6-40fe-8bce-c140ff601501
  Args:
    source: Princess_Alexandra_of_Hanover
    type: :Person
  AddTriple (529333d6-db04-4920-8778-91d79c6b028c)
 Call ID: 529333d6-db04-4920-8778-91d79c6b028c
  Args:
    relation: :hasFather
    source: Friedrich_Franz
    target: Frederick_Francis_IV
  AddTriple (0d0183a8-6dba-4ba9-9385-99cfc97b6a93)
 Call ID: 0d0183a8-6dba-4ba9-9385-99cfc97b6a93
  Args:
    source: Friedrich_Franz
    relation: :hasMother
    target: Princess_Alexandra_of_Hanover
  AssignClass (b27d848c-72e0-43bc-a4b5-02e0c8322850)
 Call ID: b27d848c-72e0-43bc-a4b5-02e0c8322850
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (2d665739-b70f-4afa-bf3a-b98701b176f9)
 Call ID: 2d665739-b70f-4afa-bf3a-b98701b176f9
  Args:
    type: :Person
    source: Ernest_Augustus_of_Hanover
  AssignClass (d2e50f3a-b5af-4677-a3a5-82e63a35d435)
 Call ID: d2e50f3a-b5af-4677-a3a5-82e63a35d435
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AssignClass (bd3e2c80-18a4-44a1-b6a8-cd27ddaf31d1)
 Call ID: bd3e2c80-18a4-44a1-b6a8-cd27ddaf31d1
  Args:
    source: Princess_Thyra_of_Denmark
    type: :Person
  AddTriple (bce6d057-0308-4465-acd8-c8c92c2d6323)
 Call ID: bce6d057-0308-4465-acd8-c8c92c2d6323
  Args:
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
    source: Princess_Alexandra_of_Hanover
  AddTriple (35936722-4c4e-46e3-8e15-6b9cd3f8d8ee)
 Call ID: 35936722-4c4e-46e3-8e15-6b9cd3f8d8ee
  Args:
    source: Princess_Alexandra_of_Hanover
    relation: :hasMother
    target: Princess_Thyra_of_Denmark
  AssignClass (8e3c481f-8b50-4b12-afec-33b8601089c2)
 Call ID: 8e3c481f-8b50-4b12-afec-33b8601089c2
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (2b1412df-3a3a-435b-a343-abee3a852b87)
 Call ID: 2b1412df-3a3a-435b-a343-abee3a852b87
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (b12db391-1bae-497b-95d1-2b8f028d2ddf)
 Call ID: b12db391-1bae-497b-95d1-2b8f028d2ddf
  Args:
    target: Christian_IX_of_Denmark
    relation: :hasFather
    source: Princess_Thyra_of_Denmark
  AssignClass (0f6f69dc-96a9-4548-97e4-2870968118f7)
 Call ID: 0f6f69dc-96a9-4548-97e4-2870968118f7
  Args:
    type: :Man
    source: Christian_Louis
  AssignClass (3c887d7d-606c-4611-929a-146d1aadf162)
 Call ID: 3c887d7d-606c-4611-929a-146d1aadf162
  Args:
    source: Christian_Louis
    type: :Person
  AddTriple (5d6e41c3-7514-4a81-843f-51f3c694cc81)
 Call ID: 5d6e41c3-7514-4a81-843f-51f3c694cc81
  Args:
    source: Friedrich_Franz
    relation: :isSiblingOf
    target: Christian_Louis
  AssignClass (7ab99cb9-31b8-4e05-be29-3619d7f6f853)
 Call ID: 7ab99cb9-31b8-4e05-be29-3619d7f6f853
  Args:
    source: Karin_Elisabeth_von_Schaper
    type: :Woman
  AssignClass (5a1e18af-8d4c-4413-8c5c-4c9eedaa9b12)
 Call ID: 5a1e18af-8d4c-4413-8c5c-4c9eedaa9b12
  Args:
    type: :Person
    source: Karin_Elisabeth_von_Schaper
  AddLiteral (8d0fcead-52fa-417b-b622-c241b407d7f7)
 Call ID: 8d0fcead-52fa-417b-b622-c241b407d7f7
  Args:
    source: Karin_Elisabeth_von_Schaper
    literal_type: xsd:integer
    literal_value: 1920
    relation: :hasBirthYear
  AddLiteral (ea78abb7-7773-4948-8ea7-3911b1884ff4)
 Call ID: ea78abb7-7773-4948-8ea7-3911b1884ff4
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2012
    source: Karin_Elisabeth_von_Schaper
  AddLiteral (72d71636-ae1d-4ca5-b030-66b19b816b3d)
 Call ID: 72d71636-ae1d-4ca5-b030-66b19b816b3d
  Args:
    literal_type: xsd:integer
    literal_value: 1941
    source: Friedrich_Franz
    relation: :hasMarriageYear
  AddTriple (5c14d217-7fdc-4528-a4b4-14b86e8ba3bd)
 Call ID: 5c14d217-7fdc-4528-a4b4-14b86e8ba3bd
  Args:
    target: Karin_Elisabeth_von_Schaper
    source: Friedrich_Franz
    relation: :hasRelation
  AssignClass (56c600c5-ebd0-4db8-94c3-746c399d35d5)
 Call ID: 56c600c5-ebd0-4db8-94c3-746c399d35d5
  Args:
    type: :Man
    source: Walter_von_Schaper
  AssignClass (ffa42e72-a7f3-4963-bbca-48acdbd24b43)
 Call ID: ffa42e72-a7f3-4963-bbca-48acdbd24b43
  Args:
    source: Walter_von_Schaper
    type: :Person
  AssignClass (845a5d41-6ab9-40d8-a0e7-0fb4903f344d)
 Call ID: 845a5d41-6ab9-40d8-a0e7-0fb4903f344d
  Args:
    source: Louise_von_Münchhausen
    type: :Woman
  AssignClass (37d15d11-a48d-4bbd-b590-7c855ac2ffd6)
 Call ID: 37d15d11-a48d-4bbd-b590-7c855ac2ffd6
  Args:
    type: :Person
    source: Louise_von_Münchhausen
  AddTriple (de539c2a-e15d-4cae-939d-428f1c363310)
 Call ID: de539c2a-e15d-4cae-939d-428f1c363310
  Args:
    source: Karin_Elisabeth_von_Schaper
    relation: :hasFather
    target: Walter_von_Schaper
  AddTriple (f9656c5f-3d50-470e-91fa-21239748e664)
 Call ID: f9656c5f-3d50-470e-91fa-21239748e664
  Args:
    target: Louise_von_Münchhausen
    relation: :hasMother
    source: Karin_Elisabeth_von_Schaper
  Finish (7f1997cb-eb96-468b-ae8c-e7a46ab731e7)
 Call ID: 7f1997cb-eb96-468b-ae8c-e7a46ab731e7
  Args: