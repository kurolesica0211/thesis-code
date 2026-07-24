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
  AssignClass (ca2e09fd-8c43-49ba-bc49-5ba8eaf9a9fc)
 Call ID: ca2e09fd-8c43-49ba-bc49-5ba8eaf9a9fc
  Args:
    type: :Man
    source: :Knud
  AssignClass (54a81d86-995b-4c5b-8e4b-364114150ae9)
 Call ID: 54a81d86-995b-4c5b-8e4b-364114150ae9
  Args:
    source: :Knud
    type: :Person
  AddLiteral (f9c7416f-61d7-4ce6-bdc6-6a1a5cf8a30c)
 Call ID: f9c7416f-61d7-4ce6-bdc6-6a1a5cf8a30c
  Args:
    relation: :hasBirthYear
    literal_value: 1900
    literal_type: xsd:integer
    source: :Knud
  AddLiteral (400692b3-d63e-4a6b-891e-8bdf9a00c4e3)
 Call ID: 400692b3-d63e-4a6b-891e-8bdf9a00c4e3
  Args:
    literal_value: 1976
    literal_type: xsd:integer
    source: :Knud
    relation: :hasDeathYear
  AssignClass (26415d50-de9d-42f0-88d1-83675a06c493)
 Call ID: 26415d50-de9d-42f0-88d1-83675a06c493
  Args:
    source: :ChristianX
    type: :Man
  AssignClass (f62da5f9-9f75-4213-96a5-5f7c52beaf4e)
 Call ID: f62da5f9-9f75-4213-96a5-5f7c52beaf4e
  Args:
    type: :Person
    source: :ChristianX
  AssignClass (4cad2c90-1c84-4ac3-89f5-f5ba11a45149)
 Call ID: 4cad2c90-1c84-4ac3-89f5-f5ba11a45149
  Args:
    type: :Woman
    source: :Alexandrine
  AssignClass (55bd05d5-0fda-4ed4-8b3b-25e4836766b4)
 Call ID: 55bd05d5-0fda-4ed4-8b3b-25e4836766b4
  Args:
    source: :Alexandrine
    type: :Person
  AddTriple (caa5663d-e044-48d7-b20a-d69cc33bea4c)
 Call ID: caa5663d-e044-48d7-b20a-d69cc33bea4c
  Args:
    source: :Knud
    target: :ChristianX
    relation: :hasFather
  AddTriple (e40e9d41-cf44-40c2-b032-6a698d2d5e6a)
 Call ID: e40e9d41-cf44-40c2-b032-6a698d2d5e6a
  Args:
    relation: :hasMother
    target: :Alexandrine
    source: :Knud
  AssignClass (a0fc9a48-3ba9-4f25-b1dc-eab82717693e)
 Call ID: a0fc9a48-3ba9-4f25-b1dc-eab82717693e
  Args:
    type: :Man
    source: :FrederikIX
  AssignClass (f7903078-2d4f-4230-8d57-8752e3a009fd)
 Call ID: f7903078-2d4f-4230-8d57-8752e3a009fd
  Args:
    type: :Person
    source: :FrederikIX
  AddTriple (cdbcf96f-3b5b-4f14-a797-ffe132752f00)
 Call ID: cdbcf96f-3b5b-4f14-a797-ffe132752f00
  Args:
    relation: :hasBrother
    source: :Knud
    target: :FrederikIX
  AssignClass (5fcee8c5-0cfb-419b-91f4-1fc9085d91c1)
 Call ID: 5fcee8c5-0cfb-419b-91f4-1fc9085d91c1
  Args:
    source: :MargretheII
    type: :Woman
  AssignClass (db722723-706e-4d67-af0c-25ca076156cf)
 Call ID: db722723-706e-4d67-af0c-25ca076156cf
  Args:
    source: :MargretheII
    type: :Person
  AddTriple (0bd99d2d-9213-4830-85a5-59218e6566ee)
 Call ID: 0bd99d2d-9213-4830-85a5-59218e6566ee
  Args:
    relation: :isFatherOf
    source: :FrederikIX
    target: :MargretheII
  AssignClass (6a73d047-63ab-4dbd-88dd-60fd01af8229)
 Call ID: 6a73d047-63ab-4dbd-88dd-60fd01af8229
  Args:
    type: :Man
    source: :Ingolf
  AssignClass (631c1f58-6341-4f35-8e9b-8594c960d256)
 Call ID: 631c1f58-6341-4f35-8e9b-8594c960d256
  Args:
    type: :Person
    source: :Ingolf
  AssignClass (6e1ca921-28dd-4c8b-810b-bac4bbcc3029)
 Call ID: 6e1ca921-28dd-4c8b-810b-bac4bbcc3029
  Args:
    source: :ChristianSonOfKnud
    type: :Man
  AssignClass (0f73292c-4b9d-4218-8495-c3eea53d68d8)
 Call ID: 0f73292c-4b9d-4218-8495-c3eea53d68d8
  Args:
    source: :ChristianSonOfKnud
    type: :Person
  AddTriple (1a9c1310-7cf2-4f40-8c40-5d8697ea5c4f)
 Call ID: 1a9c1310-7cf2-4f40-8c40-5d8697ea5c4f
  Args:
    target: :Ingolf
    source: :Knud
    relation: :hasSon
  AddTriple (a3f67a80-19c2-4525-a84d-cf69051ebaa6)
 Call ID: a3f67a80-19c2-4525-a84d-cf69051ebaa6
  Args:
    target: :ChristianSonOfKnud
    source: :Knud
    relation: :hasSon
  AssignClass (c9775aa1-26c2-4b32-b8b3-9bd655955f74)
 Call ID: c9775aa1-26c2-4b32-b8b3-9bd655955f74
  Args:
    type: :Woman
    source: :CarolineMathilde
  AssignClass (d18cbfdf-fe8c-45cc-a6da-3a44431a4229)
 Call ID: d18cbfdf-fe8c-45cc-a6da-3a44431a4229
  Args:
    source: :CarolineMathilde
    type: :Person
  AddTriple (523e72e9-ad01-47ee-8d97-0143a412df27)
 Call ID: 523e72e9-ad01-47ee-8d97-0143a412df27
  Args:
    source: :Knud
    target: :CarolineMathilde
    relation: :hasRelation
  AddLiteral (7a098db9-5dca-4acb-92bb-f722e6fae9d0)
 Call ID: 7a098db9-5dca-4acb-92bb-f722e6fae9d0
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1933
    source: :Knud
  AddTriple (0927dc9f-45f6-4942-b339-0cc629d2e5a8)
 Call ID: 0927dc9f-45f6-4942-b339-0cc629d2e5a8
  Args:
    source: :Ingolf
    target: :CarolineMathilde
    relation: :hasMother
  AddTriple (5c54e143-8f9d-451e-ad4d-80c4270a8ee7)
 Call ID: 5c54e143-8f9d-451e-ad4d-80c4270a8ee7
  Args:
    source: :ChristianSonOfKnud
    target: :CarolineMathilde
    relation: :hasMother
  AssignClass (6d31d5f0-ba8d-4289-acba-5464248ce120)
 Call ID: 6d31d5f0-ba8d-4289-acba-5464248ce120
  Args:
    type: :Woman
    source: :Elisabeth
  AssignClass (1c93cd27-729b-483c-97fa-c1061d01e9fc)
 Call ID: 1c93cd27-729b-483c-97fa-c1061d01e9fc
  Args:
    source: :Elisabeth
    type: :Person
  AddTriple (e854f1e8-c5fc-466f-80d0-1eb7fa79b1df)
 Call ID: e854f1e8-c5fc-466f-80d0-1eb7fa79b1df
  Args:
    relation: :hasDaughter
    source: :Knud
    target: :Elisabeth
  AddTriple (5155a7be-9fbd-4ffc-8c48-7cbe6f93f86f)
 Call ID: 5155a7be-9fbd-4ffc-8c48-7cbe6f93f86f
  Args:
    relation: :hasMother
    target: :CarolineMathilde
    source: :Elisabeth
  Finish (a1d9936f-98c7-41d9-a2f3-a0cbc84a784c)
 Call ID: a1d9936f-98c7-41d9-a2f3-a0cbc84a784c
  Args: