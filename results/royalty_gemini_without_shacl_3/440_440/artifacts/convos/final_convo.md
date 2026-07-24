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
  AssignClass (4220b8dc-3451-4213-8b3f-2e14bfd1f04d)
 Call ID: 4220b8dc-3451-4213-8b3f-2e14bfd1f04d
  Args:
    type: :Woman
    source: Nerissa_Bowes-Lyon
  AssignClass (e9b5dfd0-de12-479f-b136-dcc8e21622e7)
 Call ID: e9b5dfd0-de12-479f-b136-dcc8e21622e7
  Args:
    type: :Woman
    source: Katherine_Bowes-Lyon
  AssignClass (8db5f8ab-ed70-4a34-9e66-2e0bb1c2cb8e)
 Call ID: 8db5f8ab-ed70-4a34-9e66-2e0bb1c2cb8e
  Args:
    type: :Man
    source: John_Herbert_Bowes-Lyon
  AssignClass (29061968-4d78-417d-bf06-abe6e13657fa)
 Call ID: 29061968-4d78-417d-bf06-abe6e13657fa
  Args:
    type: :Woman
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AddLiteral (494e0072-af2d-416f-a1e2-7b6373e0861e)
 Call ID: 494e0072-af2d-416f-a1e2-7b6373e0861e
  Args:
    literal_value: 1919
    literal_type: xsd:integer
    source: Nerissa_Bowes-Lyon
    relation: :hasBirthYear
  AddLiteral (b11f1216-5d01-440c-82ed-4915ad720025)
 Call ID: b11f1216-5d01-440c-82ed-4915ad720025
  Args:
    literal_value: 1986
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Nerissa_Bowes-Lyon
  AddLiteral (79eba363-d969-4119-91b4-e754d56f6a76)
 Call ID: 79eba363-d969-4119-91b4-e754d56f6a76
  Args:
    literal_value: 1926
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Katherine_Bowes-Lyon
  AddLiteral (fba2dafb-9e37-4f82-9041-803daf54d285)
 Call ID: fba2dafb-9e37-4f82-9041-803daf54d285
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Katherine_Bowes-Lyon
    literal_value: 2014
  AddTriple (587fe10b-f04d-4702-ad76-22cce40c7a03)
 Call ID: 587fe10b-f04d-4702-ad76-22cce40c7a03
  Args:
    source: Nerissa_Bowes-Lyon
    relation: :hasFather
    target: John_Herbert_Bowes-Lyon
  AddTriple (c3413834-f290-469f-9dee-44350388c770)
 Call ID: c3413834-f290-469f-9dee-44350388c770
  Args:
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
    source: Nerissa_Bowes-Lyon
  AddTriple (5428e74d-6f17-4878-97b2-bc6f0dc267ee)
 Call ID: 5428e74d-6f17-4878-97b2-bc6f0dc267ee
  Args:
    target: John_Herbert_Bowes-Lyon
    source: Katherine_Bowes-Lyon
    relation: :hasFather
  AddTriple (71950332-b8d4-4a38-9acd-8554a5203e39)
 Call ID: 71950332-b8d4-4a38-9acd-8554a5203e39
  Args:
    source: Katherine_Bowes-Lyon
    relation: :hasMother
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (03001529-b498-401b-a9c0-7d6e31852c46)
 Call ID: 03001529-b498-401b-a9c0-7d6e31852c46
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AddTriple (e1534235-3227-4a37-93ea-f065d5ce081b)
 Call ID: e1534235-3227-4a37-93ea-f065d5ce081b
  Args:
    target: Queen_Elizabeth_The_Queen_Mother
    source: John_Herbert_Bowes-Lyon
    relation: :isSisterOf
  AssignClass (bac4c4ab-e826-4477-bad6-1001fd1c4f5e)
 Call ID: bac4c4ab-e826-4477-bad6-1001fd1c4f5e
  Args:
    type: :Man
    source: Claude_Bowes-Lyon_14th_Earl_of_Strathmore_and_Kinghorne
  AssignClass (abd7cd36-8cd1-49a0-923f-619a1d3f6497)
 Call ID: abd7cd36-8cd1-49a0-923f-619a1d3f6497
  Args:
    type: :Woman
    source: Cecilia_Bowes-Lyon_Countess_of_Strathmore_and_Kinghorne
  AddTriple (42ca0d60-2b32-436a-afb5-038679cef34c)
 Call ID: 42ca0d60-2b32-436a-afb5-038679cef34c
  Args:
    relation: :hasFather
    source: John_Herbert_Bowes-Lyon
    target: Claude_Bowes-Lyon_14th_Earl_of_Strathmore_and_Kinghorne
  AddTriple (69fbc5fc-9a2a-4690-a12f-13afb8d78d05)
 Call ID: 69fbc5fc-9a2a-4690-a12f-13afb8d78d05
  Args:
    target: Cecilia_Bowes-Lyon_Countess_of_Strathmore_and_Kinghorne
    source: John_Herbert_Bowes-Lyon
    relation: :hasMother
  AssignClass (2b8990d0-6ee9-482c-8667-91d4eb8e6b03)
 Call ID: 2b8990d0-6ee9-482c-8667-91d4eb8e6b03
  Args:
    type: :Man
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
  AddTriple (c5449318-1512-42bd-8dd0-d2695ffecb50)
 Call ID: c5449318-1512-42bd-8dd0-d2695ffecb50
  Args:
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasFather
    target: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
  AssignClass (17b408f6-13bc-497a-940a-7242c59ff7fa)
 Call ID: 17b408f6-13bc-497a-940a-7242c59ff7fa
  Args:
    type: :Man
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton
  AssignClass (6c83e0d9-5fab-4253-a08c-9510da6bb3eb)
 Call ID: 6c83e0d9-5fab-4253-a08c-9510da6bb3eb
  Args:
    type: :Woman
    source: Harriet_Williamina_Hepburn-Forbes
  AddTriple (79f25780-235d-4149-9708-266c53352ac4)
 Call ID: 79f25780-235d-4149-9708-266c53352ac4
  Args:
    target: Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton
    relation: :hasFather
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
  AddTriple (2b242516-8433-4bb3-bab9-3058b25b511d)
 Call ID: 2b242516-8433-4bb3-bab9-3058b25b511d
  Args:
    relation: :hasMother
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    target: Harriet_Williamina_Hepburn-Forbes
  AssignClass (805e1c7c-8965-4a11-b37d-ca7959a9622b)
 Call ID: 805e1c7c-8965-4a11-b37d-ca7959a9622b
  Args:
    type: :Woman
    source: Lady_Jane_McDonnell
  AddTriple (879732f6-d180-4b9a-8d86-7ef4e54d16c5)
 Call ID: 879732f6-d180-4b9a-8d86-7ef4e54d16c5
  Args:
    target: Lady_Jane_McDonnell
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
  AssignClass (2143c51a-15f7-451d-9822-c65c22ad4b37)
 Call ID: 2143c51a-15f7-451d-9822-c65c22ad4b37
  Args:
    type: :Woman
    source: Harriet_Hepburn-Stuart-Forbes-Trefusis
  AddTriple (60365d6a-b7f0-45b3-b8ae-a0c4ae06cbb1)
 Call ID: 60365d6a-b7f0-45b3-b8ae-a0c4ae06cbb1
  Args:
    target: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    relation: :hasFather
    source: Harriet_Hepburn-Stuart-Forbes-Trefusis
  AddTriple (4a089973-a178-459e-af65-985c82bab9f4)
 Call ID: 4a089973-a178-459e-af65-985c82bab9f4
  Args:
    relation: :hasMother
    source: Harriet_Hepburn-Stuart-Forbes-Trefusis
    target: Lady_Jane_McDonnell
  AddTriple (a759d8b5-4520-4bc0-bbd0-e054fc222ea4)
 Call ID: a759d8b5-4520-4bc0-bbd0-e054fc222ea4
  Args:
    relation: :isSisterOf
    source: Harriet_Hepburn-Stuart-Forbes-Trefusis
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
  Finish (0ad16289-6643-4856-8b57-5a7b7546b7cd)
 Call ID: 0ad16289-6643-4856-8b57-5a7b7546b7cd
  Args: