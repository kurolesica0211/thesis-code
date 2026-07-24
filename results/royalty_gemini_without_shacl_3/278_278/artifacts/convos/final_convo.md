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
  AssignClass (17418d44-3e1c-4d00-b6f2-436fa0748dfc)
 Call ID: 17418d44-3e1c-4d00-b6f2-436fa0748dfc
  Args:
    type: :Man
    source: :Knud
  AssignClass (57f2b8c0-8ac4-42c7-87d2-8cab817dbd7c)
 Call ID: 57f2b8c0-8ac4-42c7-87d2-8cab817dbd7c
  Args:
    type: :Person
    source: :Knud
  AddLiteral (944dab54-ee09-41ab-819e-c3856d635b6e)
 Call ID: 944dab54-ee09-41ab-819e-c3856d635b6e
  Args:
    relation: :hasBirthYear
    literal_value: 1900
    source: :Knud
    literal_type: xsd:integer
  AddLiteral (ef6e7aea-2410-412c-9480-b7d6e4c396e5)
 Call ID: ef6e7aea-2410-412c-9480-b7d6e4c396e5
  Args:
    literal_type: xsd:integer
    source: :Knud
    relation: :hasDeathYear
    literal_value: 1976
  AssignClass (b65d969e-acbe-4d3e-8f3f-670e5c74144d)
 Call ID: b65d969e-acbe-4d3e-8f3f-670e5c74144d
  Args:
    source: :ChristianX
    type: :Man
  AssignClass (eeed2f60-435b-4aa8-88db-d9d2ab9b97d0)
 Call ID: eeed2f60-435b-4aa8-88db-d9d2ab9b97d0
  Args:
    type: :Person
    source: :ChristianX
  AssignClass (29abc92f-2fc6-438d-a703-3ea22996bede)
 Call ID: 29abc92f-2fc6-438d-a703-3ea22996bede
  Args:
    source: :Alexandrine
    type: :Woman
  AssignClass (9a5700ed-00c5-405e-90e9-8e64ddd395d8)
 Call ID: 9a5700ed-00c5-405e-90e9-8e64ddd395d8
  Args:
    source: :Alexandrine
    type: :Person
  AddTriple (efb54628-75f2-45a5-924d-3be5bde52b65)
 Call ID: efb54628-75f2-45a5-924d-3be5bde52b65
  Args:
    relation: :hasFather
    target: :ChristianX
    source: :Knud
  AddTriple (8911d55d-4104-4169-b5fe-9d8feff3041b)
 Call ID: 8911d55d-4104-4169-b5fe-9d8feff3041b
  Args:
    relation: :hasMother
    source: :Knud
    target: :Alexandrine
  AssignClass (b8bf29af-28fc-4562-b7e2-ff78ea4dab2d)
 Call ID: b8bf29af-28fc-4562-b7e2-ff78ea4dab2d
  Args:
    type: :Man
    source: :FrederikIX
  AssignClass (e754d724-6a69-4e3c-a06b-12015fa11c21)
 Call ID: e754d724-6a69-4e3c-a06b-12015fa11c21
  Args:
    source: :FrederikIX
    type: :Person
  AddTriple (c184bcf8-c070-45e3-b997-afb8a8dace35)
 Call ID: c184bcf8-c070-45e3-b997-afb8a8dace35
  Args:
    source: :Knud
    target: :FrederikIX
    relation: :hasBrother
  AddTriple (58802f54-f988-43eb-91b5-dc5216b758e0)
 Call ID: 58802f54-f988-43eb-91b5-dc5216b758e0
  Args:
    relation: :hasFather
    target: :ChristianX
    source: :FrederikIX
  AddTriple (3964abf1-5274-41f2-bd13-87f471ccc1c7)
 Call ID: 3964abf1-5274-41f2-bd13-87f471ccc1c7
  Args:
    source: :FrederikIX
    target: :Alexandrine
    relation: :hasMother
  AssignClass (111ac0c6-4853-4915-b334-b3b6ef08bce8)
 Call ID: 111ac0c6-4853-4915-b334-b3b6ef08bce8
  Args:
    type: :Woman
    source: :CarolineMathilde
  AssignClass (8427e63c-efd1-4469-bdbe-2a474894f6d6)
 Call ID: 8427e63c-efd1-4469-bdbe-2a474894f6d6
  Args:
    source: :CarolineMathilde
    type: :Person
  AddTriple (bb82cfe2-b734-4730-9944-687a6d6b009b)
 Call ID: bb82cfe2-b734-4730-9944-687a6d6b009b
  Args:
    target: :CarolineMathilde
    source: :Knud
    relation: :hasRelation
  AddLiteral (9c7ee8a3-f422-4e05-b0ac-3ab82dc48b85)
 Call ID: 9c7ee8a3-f422-4e05-b0ac-3ab82dc48b85
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1933
    source: :Knud
  AssignClass (38977ecb-5a3b-4a99-b884-84bd07e1663a)
 Call ID: 38977ecb-5a3b-4a99-b884-84bd07e1663a
  Args:
    source: :Harald
    type: :Man
  AssignClass (393bc279-3d56-4ccf-8db0-5955387da245)
 Call ID: 393bc279-3d56-4ccf-8db0-5955387da245
  Args:
    type: :Person
    source: :Harald
  AssignClass (09df8638-5e45-4b47-b789-4f1fccdbd3e3)
 Call ID: 09df8638-5e45-4b47-b789-4f1fccdbd3e3
  Args:
    type: :Woman
    source: :Helena
  AssignClass (ac665e44-0fee-4385-8a29-cd4418fbd595)
 Call ID: ac665e44-0fee-4385-8a29-cd4418fbd595
  Args:
    type: :Person
    source: :Helena
  AddTriple (3a79305d-3a6c-49a7-8851-c8f9ec754331)
 Call ID: 3a79305d-3a6c-49a7-8851-c8f9ec754331
  Args:
    relation: :hasFather
    source: :CarolineMathilde
    target: :Harald
  AddTriple (6454f262-33b0-4bf6-b07d-f1bac61ff987)
 Call ID: 6454f262-33b0-4bf6-b07d-f1bac61ff987
  Args:
    source: :CarolineMathilde
    target: :Helena
    relation: :hasMother
  AssignClass (481df07e-8746-42ee-b28c-bac202b7e0c0)
 Call ID: 481df07e-8746-42ee-b28c-bac202b7e0c0
  Args:
    source: :Elisabeth
    type: :Woman
  AssignClass (4d2d470b-d91b-4099-8bae-0c3b101bb825)
 Call ID: 4d2d470b-d91b-4099-8bae-0c3b101bb825
  Args:
    type: :Person
    source: :Elisabeth
  AssignClass (335ef752-bcfe-4038-aa0a-e8fd1c9abadc)
 Call ID: 335ef752-bcfe-4038-aa0a-e8fd1c9abadc
  Args:
    source: :Ingolf
    type: :Man
  AssignClass (f057fea0-62c6-4f45-9e47-94787e51c62c)
 Call ID: f057fea0-62c6-4f45-9e47-94787e51c62c
  Args:
    source: :Ingolf
    type: :Person
  AssignClass (840ae49f-97d6-405e-9682-c3e7f3452ab4)
 Call ID: 840ae49f-97d6-405e-9682-c3e7f3452ab4
  Args:
    type: :Man
    source: :Christian
  AssignClass (e64b15ee-9700-409b-b3d6-03b720202dee)
 Call ID: e64b15ee-9700-409b-b3d6-03b720202dee
  Args:
    type: :Person
    source: :Christian
  AddTriple (3fb75b6f-6412-4d02-bcf6-c599665c04a5)
 Call ID: 3fb75b6f-6412-4d02-bcf6-c599665c04a5
  Args:
    relation: :hasChild
    target: :Elisabeth
    source: :Knud
  AddTriple (bb8f12bb-6f9e-421f-9965-d5234dd0921a)
 Call ID: bb8f12bb-6f9e-421f-9965-d5234dd0921a
  Args:
    source: :Knud
    target: :Ingolf
    relation: :hasChild
  AddTriple (556c36d6-acd8-43c2-949c-c50f29e78d35)
 Call ID: 556c36d6-acd8-43c2-949c-c50f29e78d35
  Args:
    relation: :hasChild
    source: :Knud
    target: :Christian
  AddTriple (bfd1c254-7268-4c58-9845-7d17f39a988e)
 Call ID: bfd1c254-7268-4c58-9845-7d17f39a988e
  Args:
    target: :Elisabeth
    source: :CarolineMathilde
    relation: :hasChild
  AddTriple (3c5fd742-d011-443b-8735-6bd666ceec17)
 Call ID: 3c5fd742-d011-443b-8735-6bd666ceec17
  Args:
    target: :Ingolf
    source: :CarolineMathilde
    relation: :hasChild
  AddTriple (67832675-33ea-4b30-b62a-1490eac7b1e4)
 Call ID: 67832675-33ea-4b30-b62a-1490eac7b1e4
  Args:
    source: :CarolineMathilde
    target: :Christian
    relation: :hasChild
  AssignClass (24974aee-57b6-4acc-9af0-e0e93300ea5b)
 Call ID: 24974aee-57b6-4acc-9af0-e0e93300ea5b
  Args:
    type: :Man
    source: :Gustav
  AssignClass (86a5da86-7fa8-4d4c-b7e8-c00b5912a720)
 Call ID: 86a5da86-7fa8-4d4c-b7e8-c00b5912a720
  Args:
    type: :Person
    source: :Gustav
  AddTriple (1a08c971-0de7-4c8d-9f26-9b4e123b8b00)
 Call ID: 1a08c971-0de7-4c8d-9f26-9b4e123b8b00
  Args:
    source: :Knud
    target: :Gustav
    relation: :hasRelation
  AssignClass (0fa0cd77-31ac-4db9-abaf-332b3587c98a)
 Call ID: 0fa0cd77-31ac-4db9-abaf-332b3587c98a
  Args:
    source: :ChristianIX
    type: :Man
  AssignClass (c351f9ee-a184-43df-aac3-36814d74f2fe)
 Call ID: c351f9ee-a184-43df-aac3-36814d74f2fe
  Args:
    source: :ChristianIX
    type: :Person
  AssignClass (ae989876-3a33-495f-b3bb-1f2d28593033)
 Call ID: ae989876-3a33-495f-b3bb-1f2d28593033
  Args:
    source: :FrederikVIII
    type: :Man
  AssignClass (a982a085-c0a4-4cff-91ec-f162cee8b75b)
 Call ID: a982a085-c0a4-4cff-91ec-f162cee8b75b
  Args:
    source: :FrederikVIII
    type: :Person
  AddTriple (ae6781a1-9efc-4dc9-943e-1d6d5a38ceab)
 Call ID: ae6781a1-9efc-4dc9-943e-1d6d5a38ceab
  Args:
    relation: :hasFather
    target: :FrederikVIII
    source: :ChristianX
  AddTriple (7eb93039-b6cd-4793-8338-ae8d46986dc9)
 Call ID: 7eb93039-b6cd-4793-8338-ae8d46986dc9
  Args:
    target: :ChristianIX
    source: :FrederikVIII
    relation: :hasFather
  AssignClass (92c2f89b-d300-41f1-abc1-a160200422a4)
 Call ID: 92c2f89b-d300-41f1-abc1-a160200422a4
  Args:
    type: :Woman
    source: :MargretheII
  AssignClass (9371003a-6131-4fd2-8428-351d5d6472f8)
 Call ID: 9371003a-6131-4fd2-8428-351d5d6472f8
  Args:
    source: :MargretheII
    type: :Person
  AddTriple (a951d018-66bd-4f6f-ac28-0670d01ca8b9)
 Call ID: a951d018-66bd-4f6f-ac28-0670d01ca8b9
  Args:
    relation: :hasFather
    source: :MargretheII
    target: :FrederikIX
  Finish (3380d559-c193-43ac-87cb-a577d2b6cd74)
 Call ID: 3380d559-c193-43ac-87cb-a577d2b6cd74
  Args: