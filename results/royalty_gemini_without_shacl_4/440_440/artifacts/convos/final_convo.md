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
  AssignClass (3224d4b6-dce0-423f-bfc8-05ef4a02df92)
 Call ID: 3224d4b6-dce0-423f-bfc8-05ef4a02df92
  Args:
    source: Nerissa Bowes-Lyon
    type: :Woman
  AssignClass (61c6e8d4-d95d-455b-a6cc-c847d7b8b96a)
 Call ID: 61c6e8d4-d95d-455b-a6cc-c847d7b8b96a
  Args:
    type: :Woman
    source: Katherine Bowes-Lyon
  AssignClass (fbfcf274-d8f5-4f35-be14-9d770a458c8f)
 Call ID: fbfcf274-d8f5-4f35-be14-9d770a458c8f
  Args:
    source: John Herbert Bowes-Lyon
    type: :Man
  AssignClass (fa023f95-8b88-4d9a-8c4a-a1c71ba4cf9e)
 Call ID: fa023f95-8b88-4d9a-8c4a-a1c71ba4cf9e
  Args:
    type: :Woman
    source: Fenella Hepburn-Stuart-Forbes-Trefusis
  AssignClass (7be0f345-5381-4578-b073-4b2cd7428384)
 Call ID: 7be0f345-5381-4578-b073-4b2cd7428384
  Args:
    source: Claude Bowes-Lyon
    type: :Man
  AssignClass (af1bcc21-6489-4516-9452-274557d84e63)
 Call ID: af1bcc21-6489-4516-9452-274557d84e63
  Args:
    source: Cecilia Bowes-Lyon
    type: :Woman
  AssignClass (b1d576ca-e09e-425e-9f79-b5579c978511)
 Call ID: b1d576ca-e09e-425e-9f79-b5579c978511
  Args:
    type: :Man
    source: Charles Hepburn-Stuart-Forbes-Trefusis (21st Baron Clinton)
  AssignClass (21745400-b274-4ff8-a68a-080a4b1c4935)
 Call ID: 21745400-b274-4ff8-a68a-080a4b1c4935
  Args:
    source: Harriet Williamina Hepburn-Forbes
    type: :Woman
  AssignClass (00821ae2-10e7-44da-9cc1-4a99b30700d7)
 Call ID: 00821ae2-10e7-44da-9cc1-4a99b30700d7
  Args:
    type: :Man
    source: Charles Hepburn-Stuart-Forbes-Trefusis (20th Baron Clinton)
  AssignClass (99194512-8b39-42fe-94a8-5bb12c4369d8)
 Call ID: 99194512-8b39-42fe-94a8-5bb12c4369d8
  Args:
    source: Lady Jane McDonnell
    type: :Woman
  AssignClass (7854fe63-ae38-4150-94ec-1e52f506bbfb)
 Call ID: 7854fe63-ae38-4150-94ec-1e52f506bbfb
  Args:
    source: Harriet Hepburn-Stuart-Forbes-Trefusis
    type: :Woman
  AssignClass (5da754f1-a1ac-43b8-bec6-0816cf704a8e)
 Call ID: 5da754f1-a1ac-43b8-bec6-0816cf704a8e
  Args:
    type: :Man
    source: Major Henry Nevile Fane
  AssignClass (604a5a1a-3547-4785-ac3e-5eb36e0a0c4f)
 Call ID: 604a5a1a-3547-4785-ac3e-5eb36e0a0c4f
  Args:
    type: :Woman
    source: Lady Elizabeth Bowes-Lyon
  AssignClass (1e466033-e543-4259-b6e7-e67d029f6fe1)
 Call ID: 1e466033-e543-4259-b6e7-e67d029f6fe1
  Args:
    source: Queen Elizabeth II
    type: :Woman
  AssignClass (1898474a-a433-4d48-9a41-cee4c1230dcc)
 Call ID: 1898474a-a433-4d48-9a41-cee4c1230dcc
  Args:
    type: :Woman
    source: Princess Margaret
  AddTriple (b2fce6e1-0192-4005-8e39-38b8a31e6957)
 Call ID: b2fce6e1-0192-4005-8e39-38b8a31e6957
  Args:
    source: Nerissa Bowes-Lyon
    relation: :hasFather
    target: John Herbert Bowes-Lyon
  AddTriple (89291054-42e9-4041-8b41-ba936e9e1cc9)
 Call ID: 89291054-42e9-4041-8b41-ba936e9e1cc9
  Args:
    source: Nerissa Bowes-Lyon
    relation: :hasMother
    target: Fenella Hepburn-Stuart-Forbes-Trefusis
  AddTriple (d671963a-87ea-4519-9119-c00d358e0df4)
 Call ID: d671963a-87ea-4519-9119-c00d358e0df4
  Args:
    source: Katherine Bowes-Lyon
    relation: :hasFather
    target: John Herbert Bowes-Lyon
  AddTriple (86f5d802-bd88-4ad3-9ecc-634894ddc927)
 Call ID: 86f5d802-bd88-4ad3-9ecc-634894ddc927
  Args:
    target: Fenella Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
    source: Katherine Bowes-Lyon
  AddTriple (9179130c-0f1f-4891-ac83-280435991f02)
 Call ID: 9179130c-0f1f-4891-ac83-280435991f02
  Args:
    target: Claude Bowes-Lyon
    relation: :hasFather
    source: John Herbert Bowes-Lyon
  AddTriple (7b2ac741-4e7b-4a28-862f-4ef3696fa0d9)
 Call ID: 7b2ac741-4e7b-4a28-862f-4ef3696fa0d9
  Args:
    relation: :hasMother
    source: John Herbert Bowes-Lyon
    target: Cecilia Bowes-Lyon
  AddTriple (95230034-18df-421c-910f-7e356a7779f2)
 Call ID: 95230034-18df-421c-910f-7e356a7779f2
  Args:
    target: Charles Hepburn-Stuart-Forbes-Trefusis (21st Baron Clinton)
    source: Fenella Hepburn-Stuart-Forbes-Trefusis
    relation: :hasFather
  AddTriple (45299fa0-5856-4095-8716-d5e6e20eee6f)
 Call ID: 45299fa0-5856-4095-8716-d5e6e20eee6f
  Args:
    target: Charles Hepburn-Stuart-Forbes-Trefusis (20th Baron Clinton)
    source: Charles Hepburn-Stuart-Forbes-Trefusis (21st Baron Clinton)
    relation: :hasFather
  AddTriple (c47385a0-ae3d-4125-bb6f-6d83b1416fde)
 Call ID: c47385a0-ae3d-4125-bb6f-6d83b1416fde
  Args:
    source: Charles Hepburn-Stuart-Forbes-Trefusis (21st Baron Clinton)
    relation: :hasMother
    target: Harriet Williamina Hepburn-Forbes
  AddTriple (bb60285d-f51e-46ba-9dd7-f78aee19fd9b)
 Call ID: bb60285d-f51e-46ba-9dd7-f78aee19fd9b
  Args:
    target: Lady Jane McDonnell
    relation: :hasMother
    source: Fenella Hepburn-Stuart-Forbes-Trefusis
  AddTriple (7cdf8f59-5628-4bd7-967c-da631428f650)
 Call ID: 7cdf8f59-5628-4bd7-967c-da631428f650
  Args:
    target: Charles Hepburn-Stuart-Forbes-Trefusis (21st Baron Clinton)
    source: Harriet Hepburn-Stuart-Forbes-Trefusis
    relation: :hasFather
  AddTriple (01d688fe-df96-4a6d-8442-88c81aeb08d8)
 Call ID: 01d688fe-df96-4a6d-8442-88c81aeb08d8
  Args:
    source: Harriet Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
    target: Lady Jane McDonnell
  AddTriple (7112c640-68a7-4abd-9b6d-1b4357981354)
 Call ID: 7112c640-68a7-4abd-9b6d-1b4357981354
  Args:
    target: Claude Bowes-Lyon
    relation: :hasFather
    source: Lady Elizabeth Bowes-Lyon
  AddTriple (74091e62-b436-4042-9e93-6fcca88eedea)
 Call ID: 74091e62-b436-4042-9e93-6fcca88eedea
  Args:
    relation: :hasMother
    source: Lady Elizabeth Bowes-Lyon
    target: Cecilia Bowes-Lyon
  AddLiteral (21170cdb-d324-4ae4-83e1-ee4ae6f9439f)
 Call ID: 21170cdb-d324-4ae4-83e1-ee4ae6f9439f
  Args:
    literal_type: xsd:string
    relation: :hasBirthYear
    literal_value: 1919
    source: Nerissa Bowes-Lyon
  AddLiteral (d35e26b4-2c93-442e-a06c-917a0df9ddde)
 Call ID: d35e26b4-2c93-442e-a06c-917a0df9ddde
  Args:
    relation: :hasDeathYear
    literal_value: 1986
    literal_type: xsd:string
    source: Nerissa Bowes-Lyon
  AddLiteral (e64611bd-fb02-47a6-89b7-821a9e6ec777)
 Call ID: e64611bd-fb02-47a6-89b7-821a9e6ec777
  Args:
    literal_type: xsd:string
    relation: :hasBirthYear
    literal_value: 1926
    source: Katherine Bowes-Lyon
  AddLiteral (420a54a9-4800-415d-a880-49975541effc)
 Call ID: 420a54a9-4800-415d-a880-49975541effc
  Args:
    source: Katherine Bowes-Lyon
    relation: :hasDeathYear
    literal_value: 2014
    literal_type: xsd:string
  Finish (954e3d22-6264-4ca4-9876-a279d5bf6228)
 Call ID: 954e3d22-6264-4ca4-9876-a279d5bf6228
  Args: