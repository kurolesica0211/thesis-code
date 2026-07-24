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
  AssignClass (3e6ffbd2-874e-42f2-a749-63359e23bbd4)
 Call ID: 3e6ffbd2-874e-42f2-a749-63359e23bbd4
  Args:
    source: :Knud
    type: :Man
  AssignClass (4373737d-e248-4192-87e7-88cc319831fd)
 Call ID: 4373737d-e248-4192-87e7-88cc319831fd
  Args:
    source: :Knud
    type: :Person
  AddLiteral (e6c4970e-2451-43df-958f-2cbf3786a739)
 Call ID: e6c4970e-2451-43df-958f-2cbf3786a739
  Args:
    relation: :hasBirthYear
    source: :Knud
    literal_value: 1900
    literal_type: xsd:integer
  AddLiteral (616b90e7-98df-4b97-9dc9-ab30a415bfdf)
 Call ID: 616b90e7-98df-4b97-9dc9-ab30a415bfdf
  Args:
    source: :Knud
    literal_value: 1976
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (d156b121-0e38-4814-a2d9-57ee8cfd8b3b)
 Call ID: d156b121-0e38-4814-a2d9-57ee8cfd8b3b
  Args:
    source: :ChristianX
    type: :Man
  AssignClass (7e1d5ea8-5fd7-4829-97d2-2cdad406ed2a)
 Call ID: 7e1d5ea8-5fd7-4829-97d2-2cdad406ed2a
  Args:
    type: :Person
    source: :ChristianX
  AssignClass (3eeb5678-a102-45b4-97cd-be708cac7f4e)
 Call ID: 3eeb5678-a102-45b4-97cd-be708cac7f4e
  Args:
    type: :Woman
    source: :Alexandrine
  AssignClass (bf906288-ed6f-4a0b-b28a-6bbf1f85607c)
 Call ID: bf906288-ed6f-4a0b-b28a-6bbf1f85607c
  Args:
    source: :Alexandrine
    type: :Person
  AddTriple (f3dfb0a5-5a71-4665-abca-609cacac2431)
 Call ID: f3dfb0a5-5a71-4665-abca-609cacac2431
  Args:
    target: :ChristianX
    source: :Knud
    relation: :hasFather
  AddTriple (07037da6-5e72-424f-9b1e-3350573f9809)
 Call ID: 07037da6-5e72-424f-9b1e-3350573f9809
  Args:
    relation: :hasMother
    target: :Alexandrine
    source: :Knud
  AssignClass (b3edafa0-bd13-4e75-ba59-50d296edab24)
 Call ID: b3edafa0-bd13-4e75-ba59-50d296edab24
  Args:
    type: :Man
    source: :FrederikIX
  AssignClass (ea38077e-0c5a-409e-a080-5522f3784430)
 Call ID: ea38077e-0c5a-409e-a080-5522f3784430
  Args:
    source: :FrederikIX
    type: :Person
  AddTriple (57506c3a-6761-402d-8dae-a14c5e404bba)
 Call ID: 57506c3a-6761-402d-8dae-a14c5e404bba
  Args:
    target: :FrederikIX
    source: :Knud
    relation: :isBrotherOf
  AssignClass (21ff2b0a-7581-4ec7-b7d9-4894f9dcd164)
 Call ID: 21ff2b0a-7581-4ec7-b7d9-4894f9dcd164
  Args:
    type: :Woman
    source: :MargretheII
  AssignClass (8124bce4-eeb8-4fe5-9e45-f31b9419843c)
 Call ID: 8124bce4-eeb8-4fe5-9e45-f31b9419843c
  Args:
    type: :Person
    source: :MargretheII
  AddTriple (d23a498a-a6a2-4fe3-8757-eaa041b0ecaf)
 Call ID: d23a498a-a6a2-4fe3-8757-eaa041b0ecaf
  Args:
    relation: :isFatherOf
    target: :MargretheII
    source: :FrederikIX
  AssignClass (762bf189-bcf8-430b-aeb8-043e7e2acbd7)
 Call ID: 762bf189-bcf8-430b-aeb8-043e7e2acbd7
  Args:
    source: :Ingolf
    type: :Man
  AssignClass (11e0b074-ce6f-4d95-81a6-6bbc0e82c8fa)
 Call ID: 11e0b074-ce6f-4d95-81a6-6bbc0e82c8fa
  Args:
    type: :Person
    source: :Ingolf
  AssignClass (7596545f-8f22-4fd9-81c6-a1f53784f873)
 Call ID: 7596545f-8f22-4fd9-81c6-a1f53784f873
  Args:
    type: :Man
    source: :ChristianSonOfKnud
  AssignClass (44d08005-fe9a-4f83-b830-71002f695dc8)
 Call ID: 44d08005-fe9a-4f83-b830-71002f695dc8
  Args:
    source: :ChristianSonOfKnud
    type: :Person
  AddTriple (eebf9a33-cf81-4f38-9798-54f9178cc2f8)
 Call ID: eebf9a33-cf81-4f38-9798-54f9178cc2f8
  Args:
    relation: :isSonOf
    target: :Knud
    source: :Ingolf
  AddTriple (90bf5968-4f21-4df1-9785-523351090257)
 Call ID: 90bf5968-4f21-4df1-9785-523351090257
  Args:
    source: :ChristianSonOfKnud
    target: :Knud
    relation: :isSonOf
  AssignClass (168467ae-1919-43f7-8134-ad6dc3503132)
 Call ID: 168467ae-1919-43f7-8134-ad6dc3503132
  Args:
    type: :Man
    source: :ChristianIX
  AssignClass (55487ba1-f8bb-4500-bd3b-3d1adb3c0d42)
 Call ID: 55487ba1-f8bb-4500-bd3b-3d1adb3c0d42
  Args:
    source: :ChristianIX
    type: :Person
  AssignClass (2045b1c1-235c-4c98-b203-e3576f5fa501)
 Call ID: 2045b1c1-235c-4c98-b203-e3576f5fa501
  Args:
    source: :FrederikVIII
    type: :Man
  AssignClass (5efdf951-16c0-4379-878f-562ccaafeee4)
 Call ID: 5efdf951-16c0-4379-878f-562ccaafeee4
  Args:
    source: :FrederikVIII
    type: :Person
  AssignClass (848e3733-1a8e-4462-8f97-ef48a4db1bb4)
 Call ID: 848e3733-1a8e-4462-8f97-ef48a4db1bb4
  Args:
    type: :Man
    source: :PrinceChristianOfDenmark
  AssignClass (2380aa74-0cb6-42c9-9d1b-86920e5027bf)
 Call ID: 2380aa74-0cb6-42c9-9d1b-86920e5027bf
  Args:
    source: :PrinceChristianOfDenmark
    type: :Person
  AssignClass (014b6ae5-ae94-4366-8330-389a66afca39)
 Call ID: 014b6ae5-ae94-4366-8330-389a66afca39
  Args:
    type: :Man
    source: :CrownPrinceFrederikOfDenmark
  AssignClass (9e184f2e-8980-4d64-a740-5a2cf1b37dbf)
 Call ID: 9e184f2e-8980-4d64-a740-5a2cf1b37dbf
  Args:
    type: :Person
    source: :CrownPrinceFrederikOfDenmark
  AddTriple (d6358837-3b01-4383-9863-44ea89de8c84)
 Call ID: d6358837-3b01-4383-9863-44ea89de8c84
  Args:
    relation: :hasFather
    source: :PrinceChristianOfDenmark
    target: :CrownPrinceFrederikOfDenmark
  AddTriple (e12aaa13-1512-49ee-b1f8-9be120722e6a)
 Call ID: e12aaa13-1512-49ee-b1f8-9be120722e6a
  Args:
    source: :Knud
    target: :PrinceChristianOfDenmark
    relation: :hasFather
  AssignClass (3798a4a1-a2ff-440f-84e8-7826cc9c889a)
 Call ID: 3798a4a1-a2ff-440f-84e8-7826cc9c889a
  Args:
    type: :Woman
    source: :CarolineMathilde
  AssignClass (b594abf4-446c-41b9-8655-faaae7604b3a)
 Call ID: b594abf4-446c-41b9-8655-faaae7604b3a
  Args:
    source: :CarolineMathilde
    type: :Person
  AddTriple (1c5d2c91-28c7-4ba0-942e-a11c0e389d75)
 Call ID: 1c5d2c91-28c7-4ba0-942e-a11c0e389d75
  Args:
    relation: :hasRelation
    target: :CarolineMathilde
    source: :Knud
  AddLiteral (acc17332-d574-4821-b8a2-620f675f2719)
 Call ID: acc17332-d574-4821-b8a2-620f675f2719
  Args:
    literal_value: 1933
    source: :Knud
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (3c3406a2-f7e7-4ac6-857a-26bc3575f6f8)
 Call ID: 3c3406a2-f7e7-4ac6-857a-26bc3575f6f8
  Args:
    type: :Man
    source: :Harald
  AssignClass (6725d14d-2e8a-44e7-8eb5-1dbeb31db11a)
 Call ID: 6725d14d-2e8a-44e7-8eb5-1dbeb31db11a
  Args:
    source: :Harald
    type: :Person
  AssignClass (6852d33b-43ca-4d6f-902c-3bb8d4eab0e3)
 Call ID: 6852d33b-43ca-4d6f-902c-3bb8d4eab0e3
  Args:
    source: :Helena
    type: :Woman
  AssignClass (bc1f5483-81b4-4b0b-a6d2-fbc15ffbda7d)
 Call ID: bc1f5483-81b4-4b0b-a6d2-fbc15ffbda7d
  Args:
    source: :Helena
    type: :Person
  AddTriple (e6863352-0e95-4f70-8930-d2ae0dc4e10a)
 Call ID: e6863352-0e95-4f70-8930-d2ae0dc4e10a
  Args:
    relation: :hasFather
    source: :CarolineMathilde
    target: :Harald
  AddTriple (c68f3787-43e5-445d-872d-c98b338663b1)
 Call ID: c68f3787-43e5-445d-872d-c98b338663b1
  Args:
    relation: :hasMother
    target: :Helena
    source: :CarolineMathilde
  AssignClass (a3de6aac-055d-4225-a8a2-3bb2a3594f29)
 Call ID: a3de6aac-055d-4225-a8a2-3bb2a3594f29
  Args:
    source: :Elisabeth
    type: :Woman
  AssignClass (439e3326-f898-4400-8b7b-ab0eb4e6dac7)
 Call ID: 439e3326-f898-4400-8b7b-ab0eb4e6dac7
  Args:
    source: :Elisabeth
    type: :Person
  AddTriple (bafad817-673f-4c86-adb4-90c1c7d6be17)
 Call ID: bafad817-673f-4c86-adb4-90c1c7d6be17
  Args:
    source: :Elisabeth
    target: :Knud
    relation: :isDaughterOf
  AddTriple (3a1dafd1-be0b-4ba1-926e-7adfe73043be)
 Call ID: 3a1dafd1-be0b-4ba1-926e-7adfe73043be
  Args:
    relation: :isDaughterOf
    target: :CarolineMathilde
    source: :Elisabeth
  AddTriple (8c2907bd-1c2d-4e95-8908-df0499a148df)
 Call ID: 8c2907bd-1c2d-4e95-8908-df0499a148df
  Args:
    source: :Ingolf
    target: :CarolineMathilde
    relation: :isSonOf
  AddTriple (15826220-3d03-46b4-90b3-989e29bacb31)
 Call ID: 15826220-3d03-46b4-90b3-989e29bacb31
  Args:
    source: :ChristianSonOfKnud
    target: :CarolineMathilde
    relation: :isSonOf
  AssignClass (725ad314-7d0a-4693-82c6-febbbd3fce57)
 Call ID: 725ad314-7d0a-4693-82c6-febbbd3fce57
  Args:
    source: :Gustav
    type: :Man
  AssignClass (0dc199ce-0ccd-45b9-88e5-e82ad8f0d318)
 Call ID: 0dc199ce-0ccd-45b9-88e5-e82ad8f0d318
  Args:
    source: :Gustav
    type: :Person
  Finish (7802d390-4bbb-435e-b634-3ac10f4aab79)
 Call ID: 7802d390-4bbb-435e-b634-3ac10f4aab79
  Args: