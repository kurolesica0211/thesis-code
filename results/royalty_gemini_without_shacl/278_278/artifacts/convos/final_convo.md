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
Knud, Hereditary Prince of Denmark (Knud Christian Frederik Michael; 27 July 1900 – 14 June 1976) was a member of the Danish royal family, the younger son and child of King Christian X and Queen Alexandrine.
From 1947 to 1953, he was heir presumptive to his older brother, King Frederik IX, and would have succeeded him as king following his death in January 1972 had it not been for a change in the Danish Act of Succession that replaced him with his niece, Queen Margrethe II.
Later, Knud's two sons, Ingolf and Christian, were stripped of their titles of prince and removed from the line of succession by the new law because they had married commoners without asking consent from their uncle.
Early life

Prince Knud was born on 27 July 1900 at his parents' country residence, the Sorgenfri Palace, located on the shores of the small river Mølleåen in Kongens Lyngby north of Copenhagen on the island of Zealand in Denmark, during the reign of his great-grandfather King Christian IX.
His parents were Prince Christian of Denmark, son of the heir apparent Crown Prince Frederik of Denmark, and Alexandrine of Mecklenburg-Schwerin.
Knud's only sibling, Prince Frederik, had been born one year before him.
Christian IX died on 29 January 1906, and Knud's grandfather succeeded him as Frederik VIII.
Six years later, on 14 May 1912, Frederik VIII died, and Knud's father ascended the throne as Christian X.


As was customary for princes at that time, Knud started a military education and entered the naval college.
Engagement and marriage

On 27 January 1933, at the age of 32, Prince Knud was engaged to his first cousin, the 20-year-old Princess Caroline-Mathilde of Denmark.
Princess Caroline-Mathilde was the second daughter of Prince Harald of Denmark and Princess Helena of Schleswig-Holstein-Sonderburg-Glücksburg, and their fathers were brothers.
The wedding was celebrated on 8 September 1933 at the chapel of Fredensborg Palace in North Zealand, Denmark.
Here they created a home for their three children: Princess Elisabeth (born in 1935), Prince Ingolf (born in 1940) and Prince Christian (born in 1944).
In 1944, Prince Knud inherited Egelund House near Fredensborg in North Zealand from his uncle, Prince Gustav of Denmark, which the couple then used as their summer residence until the hereditary prince sold it to the Danish Employers' Association in 1954.
In 1952, Prince Knud also inherited his parents' holiday residence Klitgaarden in Skagen in North Jutland from his mother, Queen Alexandrine, which the couple then used as their holiday home, and which remained in the family's possession until 1997.
Heir presumptive

On 20 April 1947, Christian X died, and Knud's brother Frederick succeeded to the throne as Frederik IX.
Since Frederik IX had fathered no sons and the Danish Act of Succession at the time followed the principle of agnatic primogeniture, Prince Knud became heir presumptive and first in line to succeed his brother as king.
Frederik IX had, however, fathered three daughters.
The new law made Frederik IX's thirteen-year-old daughter Margrethe the new heir presumptive, placing her and her two sisters before Knud and his family in the line of succession.
Later life and legacy

King Frederik IX died in 1972 and was succeeded by his daughter Queen Margrethe II.
The Princess Caroline-Mathilde Alps in Greenland were named by the 1938–39 Mørkefjord Expedition in his wife's honour for Prince Knud had been the patron of the expedition.
Prince Knud and Princess Caroline Mathilde had sat in the former royal loge at the far left of the hall (i.e., stage right), but one especially memorable scene had not been fully visible from where they had sat.



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
  AssignClass (c091c084-6c66-45c5-9c74-bddffbc80335)
 Call ID: c091c084-6c66-45c5-9c74-bddffbc80335
  Args:
    source: Knud
    type: :Man
  AssignClass (5523552c-b91a-4b4e-96f2-7c238ab03b9d)
 Call ID: 5523552c-b91a-4b4e-96f2-7c238ab03b9d
  Args:
    source: Knud
    type: :Person
  AddLiteral (c74974fa-d5e2-474f-989a-c3fd56dc30b6)
 Call ID: c74974fa-d5e2-474f-989a-c3fd56dc30b6
  Args:
    literal_value: 1900
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Knud
  AddLiteral (2467c0ae-1a93-45c6-94b4-883afc333c81)
 Call ID: 2467c0ae-1a93-45c6-94b4-883afc333c81
  Args:
    source: Knud
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1976
  AssignClass (21d657e6-a5b5-401e-9307-a870d7ffba55)
 Call ID: 21d657e6-a5b5-401e-9307-a870d7ffba55
  Args:
    source: Christian_X
    type: :Man
  AssignClass (51feab8a-e0af-4ccb-8938-ecef873ab71a)
 Call ID: 51feab8a-e0af-4ccb-8938-ecef873ab71a
  Args:
    source: Christian_X
    type: :Person
  AssignClass (5d5ae37f-1190-41f0-a26f-9e0ffee8528c)
 Call ID: 5d5ae37f-1190-41f0-a26f-9e0ffee8528c
  Args:
    source: Alexandrine
    type: :Woman
  AssignClass (7eaa28ec-0dd4-4e50-b830-b882497e3493)
 Call ID: 7eaa28ec-0dd4-4e50-b830-b882497e3493
  Args:
    source: Alexandrine
    type: :Person
  AddTriple (8f165944-de62-492c-9ab0-82024e427a42)
 Call ID: 8f165944-de62-492c-9ab0-82024e427a42
  Args:
    target: Christian_X
    relation: :hasFather
    source: Knud
  AddTriple (909a6cc9-5a1a-4f4a-93a6-ed52c2e7563c)
 Call ID: 909a6cc9-5a1a-4f4a-93a6-ed52c2e7563c
  Args:
    source: Knud
    target: Alexandrine
    relation: :hasMother
  AssignClass (cbb56034-e150-4df2-9553-42808cd8191b)
 Call ID: cbb56034-e150-4df2-9553-42808cd8191b
  Args:
    source: Frederik_IX
    type: :Man
  AssignClass (a541371d-230e-4110-8d17-0d193cee6f07)
 Call ID: a541371d-230e-4110-8d17-0d193cee6f07
  Args:
    source: Frederik_IX
    type: :Person
  AddTriple (088abbb4-0dfa-462c-9d3e-0a0f452c840a)
 Call ID: 088abbb4-0dfa-462c-9d3e-0a0f452c840a
  Args:
    target: Frederik_IX
    relation: :isBrotherOf
    source: Knud
  AssignClass (207efd09-aa4f-4a81-b54a-3a349f278829)
 Call ID: 207efd09-aa4f-4a81-b54a-3a349f278829
  Args:
    source: Caroline-Mathilde
    type: :Woman
  AssignClass (59a64868-2f8d-4fb8-bd09-34f6e9bd57f5)
 Call ID: 59a64868-2f8d-4fb8-bd09-34f6e9bd57f5
  Args:
    source: Caroline-Mathilde
    type: :Person
  AddTriple (b7d6514a-f839-4767-ba04-37f1843a7bfd)
 Call ID: b7d6514a-f839-4767-ba04-37f1843a7bfd
  Args:
    relation: :hasRelation
    target: Caroline-Mathilde
    source: Knud
  AddLiteral (9c0ded74-34b2-4e48-8a6a-103f68daddf2)
 Call ID: 9c0ded74-34b2-4e48-8a6a-103f68daddf2
  Args:
    literal_type: xsd:integer
    source: Knud
    literal_value: 1933
    relation: :hasMarriageYear
  AssignClass (c035ff7f-da90-470d-b440-e935385ccc8a)
 Call ID: c035ff7f-da90-470d-b440-e935385ccc8a
  Args:
    source: Harald
    type: :Man
  AssignClass (8c01805f-59eb-4b8b-94c4-eb6f630f7f3f)
 Call ID: 8c01805f-59eb-4b8b-94c4-eb6f630f7f3f
  Args:
    source: Harald
    type: :Person
  AssignClass (5f870b13-bf12-4582-8a97-67a22d67292b)
 Call ID: 5f870b13-bf12-4582-8a97-67a22d67292b
  Args:
    source: Helena
    type: :Woman
  AssignClass (a3186391-fe8f-42d9-8a08-11da69393bfd)
 Call ID: a3186391-fe8f-42d9-8a08-11da69393bfd
  Args:
    source: Helena
    type: :Person
  AddTriple (fc6956b0-0757-434a-9445-04454ff709aa)
 Call ID: fc6956b0-0757-434a-9445-04454ff709aa
  Args:
    source: Caroline-Mathilde
    relation: :hasFather
    target: Harald
  AddTriple (b6701af7-b5d2-40a4-b2c1-174927147ca2)
 Call ID: b6701af7-b5d2-40a4-b2c1-174927147ca2
  Args:
    source: Caroline-Mathilde
    target: Helena
    relation: :hasMother
  AssignClass (5a42f9e5-5651-4d3e-95ff-a0d34c9dba2d)
 Call ID: 5a42f9e5-5651-4d3e-95ff-a0d34c9dba2d
  Args:
    source: Elisabeth
    type: :Woman
  AssignClass (d3501105-60f3-46e9-a239-904b3d60375c)
 Call ID: d3501105-60f3-46e9-a239-904b3d60375c
  Args:
    source: Elisabeth
    type: :Person
  AssignClass (bd3d39fc-ff85-4201-9c4d-030d35c03e06)
 Call ID: bd3d39fc-ff85-4201-9c4d-030d35c03e06
  Args:
    source: Ingolf
    type: :Man
  AssignClass (471c57df-497f-461f-b29e-e42121fb0032)
 Call ID: 471c57df-497f-461f-b29e-e42121fb0032
  Args:
    source: Ingolf
    type: :Person
  AssignClass (be247594-e76c-4993-b7cc-ce232eae7f57)
 Call ID: be247594-e76c-4993-b7cc-ce232eae7f57
  Args:
    source: Christian_son_of_Knud
    type: :Man
  AssignClass (cff17160-e0f1-41e8-923b-0e4dd25cf57b)
 Call ID: cff17160-e0f1-41e8-923b-0e4dd25cf57b
  Args:
    source: Christian_son_of_Knud
    type: :Person
  AddTriple (5d2da082-b542-44ed-9182-066cb469ae36)
 Call ID: 5d2da082-b542-44ed-9182-066cb469ae36
  Args:
    source: Knud
    relation: :hasChild
    target: Elisabeth
  AddTriple (5de6a86b-7c76-47d9-8b0b-adcd23507fc0)
 Call ID: 5de6a86b-7c76-47d9-8b0b-adcd23507fc0
  Args:
    relation: :hasChild
    target: Ingolf
    source: Knud
  AddTriple (1a5a8701-6e3d-43d1-b7ca-94b2a8829967)
 Call ID: 1a5a8701-6e3d-43d1-b7ca-94b2a8829967
  Args:
    source: Knud
    relation: :hasChild
    target: Christian_son_of_Knud
  AddTriple (d69b0590-f3f0-40f9-9332-e26c70c0b330)
 Call ID: d69b0590-f3f0-40f9-9332-e26c70c0b330
  Args:
    source: Caroline-Mathilde
    relation: :hasChild
    target: Elisabeth
  AddTriple (9d04ebca-a3bb-48a9-88b4-b15f72bcaf89)
 Call ID: 9d04ebca-a3bb-48a9-88b4-b15f72bcaf89
  Args:
    relation: :hasChild
    target: Ingolf
    source: Caroline-Mathilde
  AddTriple (b13c9a4b-6ac6-412a-a822-674f4ce38248)
 Call ID: b13c9a4b-6ac6-412a-a822-674f4ce38248
  Args:
    source: Caroline-Mathilde
    relation: :hasChild
    target: Christian_son_of_Knud
  AssignClass (13defa10-db98-4fff-ae83-d9aba38999bf)
 Call ID: 13defa10-db98-4fff-ae83-d9aba38999bf
  Args:
    source: Gustav
    type: :Man
  AssignClass (ea66ddb5-63ef-4d62-b454-e0e8e07f0cca)
 Call ID: ea66ddb5-63ef-4d62-b454-e0e8e07f0cca
  Args:
    source: Gustav
    type: :Person
  AssignClass (dfdf25db-630a-4d28-b705-d73b19954842)
 Call ID: dfdf25db-630a-4d28-b705-d73b19954842
  Args:
    source: Margrethe_II
    type: :Woman
  AssignClass (65091fcf-5c1b-4a1d-b4a9-0621689e5d3a)
 Call ID: 65091fcf-5c1b-4a1d-b4a9-0621689e5d3a
  Args:
    source: Margrethe_II
    type: :Person
  AddTriple (5fb20a8d-fe8b-4f71-93a5-2e88c6c3f85a)
 Call ID: 5fb20a8d-fe8b-4f71-93a5-2e88c6c3f85a
  Args:
    source: Margrethe_II
    relation: :isChildOf
    target: Frederik_IX
  Finish (9cf0f480-7949-4a14-bb2a-c6322e24c4d3)
 Call ID: 9cf0f480-7949-4a14-bb2a-c6322e24c4d3
  Args: