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
Nerissa Jane Irene Bowes-Lyon (18 February 1919 – 22 January 1986) and Katherine Juliet Bowes-Lyon (4 July 1926 – 23 February 2014) were two mentally disabled daughters of John Herbert Bowes-Lyon and his wife Fenella (née Hepburn-Stuart-Forbes-Trefusis).
John was the brother of Queen Elizabeth the Queen Mother, thus his two daughters were the maternal first cousins of Queen Elizabeth II and Princess Margaret, sharing one pair of grandparents, Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne, and Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne.
Background

Nerissa Bowes-Lyon was born on 18 February 1919 and Katherine Bowes-Lyon was born on 4 July 1926, the daughters of John Herbert Bowes-Lyon and Fenella Hepburn-Stuart-Forbes-Trefusis.
Their father, the second son of Claude Bowes-Lyon, 14th Earl of Strathmore and Kinghorne, was a brother of Lady Elizabeth Bowes-Lyon, Duchess of York, the future Queen Elizabeth II's mother.
Their mother was the younger daughter of Charles Hepburn-Stuart-Forbes-Trefusis, 21st Baron Clinton.
The sisters’ maternal great-grandparents Charles Hepburn-Stuart-Forbes-Trefusis, 20th Baron Clinton and his wife Harriet Williamina Hepburn-Forbes had been first cousins and their son (the sisters maternal grand-father)
Charles Hepburn-Stuart-Forbes-Trefusis, 21st Baron Clinton, married his second cousin once removed Lady Jane McDonnell.
Their father died 7 February 1930 after having contracted pneumonia at the age of 43, leaving their mother alone to care for their four young children.
The 1963 edition of Burke's Peerage listed Nerissa and Katherine as having died in 1940 and 1961 respectively; but in 1987 it was revealed by The Sun that the sisters were alive, and had been placed in Earlswood Hospital for mentally disabled people in 1941.
Nerissa died in 1986, aged 66, with only hospital staff attending the funeral, while Katherine died in 2014, aged 87.
Controversy

Suggestions of a cover-up were rejected in the press by Lord Clinton in 1987, who claimed that his aunt Fenella (the mother of the two women) had completed the form for Burke's incorrectly due to Fenella being "a vague person"; however, Burke's included specific dates of death for both sisters.
According to a 2011 television documentary about the sisters, The Queen's Hidden Cousins, broadcast by Channel 4, "throughout their time at the hospital, there is no known record that the sisters were ever visited by any member of the Bowes-Lyon or royal families, despite their aunt, the Queen Mother, being a Patron of Mencap" (a charity for people with learning disabilities).
When Nerissa died in 1986, none of her family attended the funeral.
Sources from within the family, however, report that their mother Fenella often visited the two sisters until her death in 1966; Lady Elizabeth Shakerley, Fenella's granddaughter, also said other members of the family had often visited over the years and had often sent gifts and cards on Christmas and birthdays.
Queen Elizabeth The Queen Mother, upon discovering that her nieces were alive in 1982, sent money for toys and sweets on their birthdays and at Christmas.
The three grandchildren of Fenella and John (Lady Elizabeth Shakerley, the 5th Earl of Lichfield, and Katherine Somervell) organised the headstone for Nerissa Bowes-Lyon.
Harriet Hepburn-Stuart-Forbes-Trefusis (1887–1958), sister of Nerissa and Katherine's mother Fenella, married Major Henry Nevile Fane, and three of their seven children lived in Earlswood Hospital.
David Danks, then director of the Murdoch Children's Research Institute, thought that a genetic disease in the Hepburn-Stuart-Forbes-Trefusis family may have been the cause of death of some male family members in early childhood and caused learning disabilities in some female family members.
According to Lady Colin Campbell, whose mother was a friend of a doctor who treated the sisters, they suffered from Huntington's disease.
Anne Tennant, Baroness Glenconner was, as a young woman and 1950s debutante of the year, engaged to Johnnie, Viscount Althorp, later the Earl Spencer and father to Diana, Princess of Wales; his father objected to the match on the grounds of "mad blood", as one of her grandmothers was a Trefusis, and the engagement was broken off.
The Queen's Hidden Cousins

In November 2011, Channel 4 broadcast a documentary about the sisters, The Queen's Hidden Cousins.
The documentary was directed by Kelly Close and made by Minnow Films, an independent production company, whose synopsis states that "Whilst their sisters Elizabeth and Anne enjoyed lives of privilege and inclusion in the upper echelons of the aristocracy, Katherine and Nerissa were all but forgotten, written out of family history."
"


Prior to the screening, the Daily Express reported that the Queen was said to be "hugely distressed" by it.
Lady Elizabeth Shakerley, party planner to the Queen and the sisters' niece, responded at length, disputing both the assertions by the programme-makers of familial abandonment and the methods of "this supposedly factual documentary".
She called it "cruel" and "intrusive" and said that "far from being a taboo subject, Katherine and Nerissa were very much a part of the family as sisters of Shakerley's mother, the late Princess Anne of Denmark.
Following the programme's broadcast, The Guardian's reviewer John Crace wrote that "All we learned was just common knowledge."
Crace observed that it was Nerissa's death in 1986 which had sparked the tabloid interest in the story the following year.



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
  AssignClass (e620130b-0e00-46d1-bed6-b4f629bb7051)
 Call ID: e620130b-0e00-46d1-bed6-b4f629bb7051
  Args:
    source: Nerissa_Bowes-Lyon
    type: :Woman
  AssignClass (3c0d8b2f-0bda-4f6c-b679-fb13a80f7728)
 Call ID: 3c0d8b2f-0bda-4f6c-b679-fb13a80f7728
  Args:
    source: Katherine_Bowes-Lyon
    type: :Woman
  AssignClass (ec29c1ab-d0e6-4519-ab72-df51af95b8a0)
 Call ID: ec29c1ab-d0e6-4519-ab72-df51af95b8a0
  Args:
    source: John_Herbert_Bowes-Lyon
    type: :Man
  AssignClass (eb975bd7-cb04-4599-b4c8-ea67bed5fe1e)
 Call ID: eb975bd7-cb04-4599-b4c8-ea67bed5fe1e
  Args:
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
    type: :Woman
  AssignClass (dfa54d30-9a95-4c3c-adf1-6277229b6101)
 Call ID: dfa54d30-9a95-4c3c-adf1-6277229b6101
  Args:
    source: Claude_Bowes-Lyon
    type: :Man
  AssignClass (cd0f013f-f967-42f6-b4b8-671a2be8d784)
 Call ID: cd0f013f-f967-42f6-b4b8-671a2be8d784
  Args:
    source: Cecilia_Bowes-Lyon
    type: :Woman
  AssignClass (bcd58020-b4c7-4792-b2da-e70e5e3a0256)
 Call ID: bcd58020-b4c7-4792-b2da-e70e5e3a0256
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    type: :Man
  AssignClass (cf686a3d-fc05-4d85-b5aa-01168bdf0a8d)
 Call ID: cf686a3d-fc05-4d85-b5aa-01168bdf0a8d
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton
    type: :Man
  AssignClass (89bb2ac7-d0bc-46e0-81fb-294ca0a4f8aa)
 Call ID: 89bb2ac7-d0bc-46e0-81fb-294ca0a4f8aa
  Args:
    source: Harriet_Williamina_Hepburn-Forbes
    type: :Woman
  AssignClass (861144cf-3779-49ba-aa92-7fc9f7a43327)
 Call ID: 861144cf-3779-49ba-aa92-7fc9f7a43327
  Args:
    source: Lady_Jane_McDonnell
    type: :Woman
  AddLiteral (b0de525d-ab9a-4d19-8751-db4c6a01a84c)
 Call ID: b0de525d-ab9a-4d19-8751-db4c6a01a84c
  Args:
    literal_type: xsd:integer
    source: Nerissa_Bowes-Lyon
    literal_value: 1919
    relation: :hasBirthYear
  AddLiteral (56a642dd-2f8a-4441-88c8-0fc0403e61cd)
 Call ID: 56a642dd-2f8a-4441-88c8-0fc0403e61cd
  Args:
    source: Nerissa_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1986
    relation: :hasDeathYear
  AddLiteral (1b71994a-5eb2-402b-93f2-f6231dc2f04c)
 Call ID: 1b71994a-5eb2-402b-93f2-f6231dc2f04c
  Args:
    literal_value: 1926
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Katherine_Bowes-Lyon
  AddLiteral (ec451f96-c41d-45a9-b9c2-0ca56425839d)
 Call ID: ec451f96-c41d-45a9-b9c2-0ca56425839d
  Args:
    relation: :hasDeathYear
    literal_value: 2014
    source: Katherine_Bowes-Lyon
    literal_type: xsd:integer
  AddTriple (11c9ee3a-8c9b-43fd-8cbf-35450ec85100)
 Call ID: 11c9ee3a-8c9b-43fd-8cbf-35450ec85100
  Args:
    source: Nerissa_Bowes-Lyon
    relation: :hasFather
    target: John_Herbert_Bowes-Lyon
  AddTriple (ae02991f-a4db-4876-b726-20c967a20e44)
 Call ID: ae02991f-a4db-4876-b726-20c967a20e44
  Args:
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
    source: Nerissa_Bowes-Lyon
  AddTriple (d0b53608-a981-41a9-83b8-3297ec09d056)
 Call ID: d0b53608-a981-41a9-83b8-3297ec09d056
  Args:
    source: Katherine_Bowes-Lyon
    relation: :hasFather
    target: John_Herbert_Bowes-Lyon
  AddTriple (3793f1c2-7113-4a03-81cf-6bd1249e5830)
 Call ID: 3793f1c2-7113-4a03-81cf-6bd1249e5830
  Args:
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
    source: Katherine_Bowes-Lyon
  AddTriple (54f72e28-3a17-4aa8-a6c2-8724f244a69e)
 Call ID: 54f72e28-3a17-4aa8-a6c2-8724f244a69e
  Args:
    source: John_Herbert_Bowes-Lyon
    relation: :hasFather
    target: Claude_Bowes-Lyon
  AddTriple (9c4ca7f3-8dae-4f9b-bbcb-58036f21ccbe)
 Call ID: 9c4ca7f3-8dae-4f9b-bbcb-58036f21ccbe
  Args:
    relation: :hasMother
    target: Cecilia_Bowes-Lyon
    source: John_Herbert_Bowes-Lyon
  AddTriple (12b98de5-2bb8-428f-89a0-8a463c4e1bbb)
 Call ID: 12b98de5-2bb8-428f-89a0-8a463c4e1bbb
  Args:
    relation: :hasFather
    target: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AddTriple (2a44aa3b-2c3b-4347-9ea4-33c828ad816f)
 Call ID: 2a44aa3b-2c3b-4347-9ea4-33c828ad816f
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    target: Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton
    relation: :hasFather
  AddTriple (b4a743e3-c936-4666-8f8c-f5220cf87a2a)
 Call ID: b4a743e3-c936-4666-8f8c-f5220cf87a2a
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    relation: :hasMother
    target: Harriet_Williamina_Hepburn-Forbes
  AddTriple (a4d0dd03-c751-424a-8709-3e9b4f3f3273)
 Call ID: a4d0dd03-c751-424a-8709-3e9b4f3f3273
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton
    target: Harriet_Williamina_Hepburn-Forbes
    relation: :hasMother
  AddTriple (547bd2d1-bbae-43fb-9196-d8205bd40d90)
 Call ID: 547bd2d1-bbae-43fb-9196-d8205bd40d90
  Args:
    target: Lady_Jane_McDonnell
    relation: :hasMother
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
  Finish (9e1ac248-0eb4-44ef-9549-1e4ffec0d681)
 Call ID: 9e1ac248-0eb4-44ef-9549-1e4ffec0d681
  Args: