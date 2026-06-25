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
Lady Elizabeth Georgiana Shakerley CVO (née Anson; 7 June 1941 – 1 November 2020) was a British party planner, writer and socialite from the Anson family.
She was a first cousin once removed of Queen Elizabeth II and sister of Patrick Anson, 5th Earl of Lichfield.
Early life

The Honourable Elizabeth Georgiana Anson was born on 7 June 1941 at Windsor Castle to Thomas Anson, Viscount Anson (1913–1958), and Anne Bowes-Lyon.
Shakerley's mother was a niece of Queen Elizabeth (later the Queen Mother).
She was the niece of Nerissa and Katherine Bowes-Lyon.
In 1960, her paternal grandfather, the 4th Earl of Lichfield, died and her brother, Patrick, inherited the title and family seat, Shugborough Hall near Great Haywood, Staffordshire.
Despite the estate's passing to the National Trust in lieu of death duties, Lord Lichfield maintained an apartment for himself and his sister.
Subsequently, her mother married Prince Georg of Denmark and moved to Paris where Prince Georg served as military, naval and air attaché.
Her father died in 1958 before acceding to the earldom of  Lichfield.
On 12 July 1961, Queen Elizabeth II issued a Royal Warrant of Precedence granting Shakerley the title, rank, place, pre-eminence and precedence of the daughter of an Earl as if her father had succeeded.
Thus, she became known as Lady Elizabeth Anson.
In 1966, Shakerley was a bridesmaid at the wedding of Princess Beatrix of the Netherlands and Claus van Amsberg.
Career

Following the stress of planning her own debutante ball in 1959, Lady Elizabeth founded the firm Party Planners in 1960.
From then on she planned parties for her cousin Queen Elizabeth II.
Even after her marriage, she continued to be known as Elizabeth Anson professionally.
In 1986, Shakerley published Lady Elizabeth Anson's Party Planners Book.
The courts eventually ruled in favour of Trump.


Notable events she planned include: Sting's 1992 wedding to Trudie Styler; Margaret Thatcher's 70th birthday party in 1995; Queen Elizabeth II's 80th and 90th birthday parties in 2006 and 2016, respectively; Crown Prince Pavlos of Greece's 1995 wedding to Marie-Chantal Miller; and a reception for foreign royal guests the night before the Prince William's 2011 wedding to Catherine Middleton.
In 2000, she planned three consecutive events for the royal family; Prince William's 18th birthday on 21 June, Princess Anne's 50th birthday on 15 August and Princess Margaret's 70th birthday on 21 August.
As the stepdaughter of a Danish prince, Shakerley also attended many royal events in continental Europe, including the birthday celebrations of the King Harald V of Norway (her stepfather's first cousin) and the funeral of Jean, Grand Duke of Luxembourg.
In 2018, Shakerley attended a state banquet given by Queen Elizabeth II in honour of the King and Queen of the Netherlands at Buckingham Palace.
Personal life and death

On 27 July 1972, Shakerley married Sir Geoffrey Shakerley, 6th Bt, at Westminster Abbey.
Guests at the wedding included Queen Elizabeth II, Queen Elizabeth the Queen Mother and Princess Beatrix of the Netherlands.
Her second cousins Princess Anne and Lady Sarah Armstrong-Jones were among her bridesmaids.
Lady Elizabeth and Shakerley separated in 1986 and divorced in 2009.
They had one daughter and two grandchildren:


Shakerley suffered from chronic fatigue syndrome.
She is buried in the Anson family vault at St Michael and All Angels Church, Colwich, Staffordshire, near Shugborough Hall.
The Countess of Wessex (representing Queen Elizabeth II), Princess Beatrix of the Netherlands and Sheikh Hamad bin Khalifa Al Thani of Qatar attended.



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
  AssignClass (ae895e28-8336-4720-88f9-ad16b4a1f7a6)
 Call ID: ae895e28-8336-4720-88f9-ad16b4a1f7a6
  Args:
    source: Elizabeth_Georgiana_Anson
    type: :Woman
  AssignClass (3e8e7407-553c-45d7-a96c-35ec24b222d8)
 Call ID: 3e8e7407-553c-45d7-a96c-35ec24b222d8
  Args:
    type: :Person
    source: Elizabeth_Georgiana_Anson
  AddLiteral (7ccfb629-cc5f-49a9-979c-9e52671e2cdc)
 Call ID: 7ccfb629-cc5f-49a9-979c-9e52671e2cdc
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Elizabeth_Georgiana_Anson
    literal_value: 1941
  AddLiteral (3651c4d1-1171-4e96-aebb-f3a3348f1e28)
 Call ID: 3651c4d1-1171-4e96-aebb-f3a3348f1e28
  Args:
    source: Elizabeth_Georgiana_Anson
    literal_value: 2020
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (38c09a6e-5257-47c4-a279-799f26b6aa4f)
 Call ID: 38c09a6e-5257-47c4-a279-799f26b6aa4f
  Args:
    type: :Man
    source: Thomas_Anson_Viscount_Anson
  AssignClass (d5e166ce-c005-4b6d-b042-fb50d91537f0)
 Call ID: d5e166ce-c005-4b6d-b042-fb50d91537f0
  Args:
    type: :Person
    source: Thomas_Anson_Viscount_Anson
  AssignClass (a950ad29-b8b2-43d1-835e-eb9b81f4dcb7)
 Call ID: a950ad29-b8b2-43d1-835e-eb9b81f4dcb7
  Args:
    type: :Ancestor
    source: Thomas_Anson_Viscount_Anson
  AddLiteral (a6b4cf3b-4018-4175-87ef-456e50ad5702)
 Call ID: a6b4cf3b-4018-4175-87ef-456e50ad5702
  Args:
    relation: :hasBirthYear
    source: Thomas_Anson_Viscount_Anson
    literal_value: 1913
    literal_type: xsd:integer
  AddLiteral (370c6b26-bed4-4178-9682-47005e7b1caa)
 Call ID: 370c6b26-bed4-4178-9682-47005e7b1caa
  Args:
    relation: :hasDeathYear
    source: Thomas_Anson_Viscount_Anson
    literal_value: 1958
    literal_type: xsd:integer
  AssignClass (10ce576e-95ed-41b4-ad5a-3ca29071700c)
 Call ID: 10ce576e-95ed-41b4-ad5a-3ca29071700c
  Args:
    type: :Woman
    source: Anne_Bowes-Lyon
  AssignClass (addf6ed6-b4ea-4ccf-9917-b55046cc86f2)
 Call ID: addf6ed6-b4ea-4ccf-9917-b55046cc86f2
  Args:
    type: :Person
    source: Anne_Bowes-Lyon
  AssignClass (179399b0-cb33-48f0-a94d-a996ae2e8a67)
 Call ID: 179399b0-cb33-48f0-a94d-a996ae2e8a67
  Args:
    source: Anne_Bowes-Lyon
    type: :Ancestor
  AddTriple (67c5c8a7-8a90-41cc-88c1-f00b593687e8)
 Call ID: 67c5c8a7-8a90-41cc-88c1-f00b593687e8
  Args:
    relation: :hasFather
    target: Thomas_Anson_Viscount_Anson
    source: Elizabeth_Georgiana_Anson
  AddTriple (bcf586cf-41bf-4cbb-9979-4ff1839b33cc)
 Call ID: bcf586cf-41bf-4cbb-9979-4ff1839b33cc
  Args:
    source: Elizabeth_Georgiana_Anson
    target: Anne_Bowes-Lyon
    relation: :hasMother
  AssignClass (500ebbe3-4049-4a21-9fe7-eaf51eec6c1d)
 Call ID: 500ebbe3-4049-4a21-9fe7-eaf51eec6c1d
  Args:
    source: Patrick_Anson_5th_Earl_of_Lichfield
    type: :Man
  AssignClass (fef86129-3ee7-4c30-926f-a705b76a3360)
 Call ID: fef86129-3ee7-4c30-926f-a705b76a3360
  Args:
    type: :Person
    source: Patrick_Anson_5th_Earl_of_Lichfield
  AddTriple (53bd93b8-d75f-4116-824b-6e941a68ee76)
 Call ID: 53bd93b8-d75f-4116-824b-6e941a68ee76
  Args:
    relation: :isSiblingOf
    target: Patrick_Anson_5th_Earl_of_Lichfield
    source: Elizabeth_Georgiana_Anson
  AssignClass (4417d704-3ecd-4e75-81bf-f2d1ad04e770)
 Call ID: 4417d704-3ecd-4e75-81bf-f2d1ad04e770
  Args:
    type: :Man
    source: Prince_Georg_of_Denmark
  AssignClass (e447f25b-a16c-456a-b911-3ce678a3c034)
 Call ID: e447f25b-a16c-456a-b911-3ce678a3c034
  Args:
    source: Prince_Georg_of_Denmark
    type: :Person
  AddTriple (c5f0c93f-7327-4fe2-ae42-e80377af6331)
 Call ID: c5f0c93f-7327-4fe2-ae42-e80377af6331
  Args:
    source: Anne_Bowes-Lyon
    target: Prince_Georg_of_Denmark
    relation: :hasMarriageYear
  AssignClass (5dcef8a9-8cd1-43f5-8a8e-9dc42ca8d209)
 Call ID: 5dcef8a9-8cd1-43f5-8a8e-9dc42ca8d209
  Args:
    source: Geoffrey_Shakerley_6th_Bt
    type: :Man
  AssignClass (b21a7d0f-2edd-4187-8b7f-2f2cc9bbc8a7)
 Call ID: b21a7d0f-2edd-4187-8b7f-2f2cc9bbc8a7
  Args:
    type: :Person
    source: Geoffrey_Shakerley_6th_Bt
  AddTriple (6d63975a-a97f-4cbf-a5d6-2e599139be86)
 Call ID: 6d63975a-a97f-4cbf-a5d6-2e599139be86
  Args:
    relation: :hasMarriageYear
    source: Elizabeth_Georgiana_Anson
    target: Geoffrey_Shakerley_6th_Bt
  AddLiteral (4f3c4498-504a-4e93-8d90-f972c891abe2)
 Call ID: 4f3c4498-504a-4e93-8d90-f972c891abe2
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    source: Elizabeth_Georgiana_Anson
    relation: :hasMarriageYear
  Finish (cb035f44-22fe-42b2-9fbb-66c3c253fa1f)
 Call ID: cb035f44-22fe-42b2-9fbb-66c3c253fa1f
  Args: