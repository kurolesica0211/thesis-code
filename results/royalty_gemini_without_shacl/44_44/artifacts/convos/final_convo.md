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
Queen Margrethe II


Princess Isabella of Denmark, Countess of Monpezat, RE (Isabella Henrietta Ingrid Margrethe; born 21 April 2007) is a member of the Danish royal family.
She is the second child and elder daughter of King Frederik X and Queen Mary.
She is the fourth grandchild and oldest granddaughter of Queen Margrethe II and Prince Henrik.
Isabella is second in the line of succession to the Danish throne, after her older brother, Crown Prince Christian.
Early life and education

Isabella was born on 21 April 2007 at 4:02 pm CET at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, to then Crown Prince Frederik and Crown Princess Mary.
Incidentally, Isabella was the first princess whose birth was marked with 21 shots, as the number of shots in the cannon salute had previously been different depending on the sex of the newborn, as 21 shots were fired for a boy and 17 shots for a girl.
But before Prince Christian was born in October 2005, the palace decided that 21 shots should be fired, regardless of the child's sex.
Her christening took place on 1 July 2007 at the Royal Chapel of Fredensborg Palace and was performed by the Bishop of Copenhagen Erik Norman Svendsen.
She was baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671, and wore the royal christening gown which was made for her great-great-grandfather, King Christian X, in 1870.
At the christening, her name, per Danish royal tradition, was revealed to be Isabella Henrietta Ingrid Margrethe, after the Danish queen consort and ancestress Isabella of Austria, the princess's maternal grandmother, paternal great-grandmother, and paternal grandmother respectively.
Her godparents were her father's first cousin, Princess Alexia of Greece and Denmark; Queen Mathilde of Belgium (then Duchess of Brabant), Nadine Johnston, Christian Buchwald, Peter Heering and Marie Louise Skeel.
Isabella received the Lutheran rite of confirmation in the same chapel on 30 April 2022, which was presided over by Henrik Wigh-Poulsen, the Danish royal Chaplain-in-Ordinary.
With the passing of the 2009 Danish Act of Succession referendum, Isabella became the first princess in Danish history to not get bypassed by a younger brother when Prince Vincent was born in 2011.
On 13 August 2013, Isabella started school at Tranegårdsskolen in Gentofte, the same public school as her older brother.
In January 2020, Isabella and her three siblings initiated a 12-week school stay at Lemania-Verbier International School in Verbier, Switzerland.
The stay was eventually cut short and the siblings returned home in March due to the intensification of the COVID-19 situation in Denmark.
In March 2022, it was announced that Isabella would continue her education at Herlufsholm School starting in August 2022.
However, on 26 June 2022, her parents announced in a statement that Isabella would not start Herlufsholm after all due to revelations of recurring problems of bullying, violence and sexual abuse at the school, and in September 2022, she started 9th form at Ingrid Jespersens Gymnasieskole in Copenhagen instead.
In August 2023, Isabella started upper secondary school at Øregård Gymnasium – the same school her father, Frederik, and uncle, Joachim, previously attended.
In March 2026, it was announced that Isabella will undertake conscription with the Guard Hussar Regiment in the Royal Danish Army starting August 2026.
Previously, Queen Margrethe II performed voluntary service with the Women's Flying Corps, a branch of the Danish Home Guard, between 1958 and 1970, and Queen Mary has also trained with the Home Guard, but neither have undergone formal training with the armed forces.
Public life

Isabella undertook her first official engagement, the baptism of a ferry – the M/F Prinsesse Isabella operating between Jutland and Samsø – named in her honour, on 6 June 2015.
During the reception, Isabella made her first ever public speech, thanking the city and the participants for a "very unique" birthday celebration.
On 15 April, the Danish court and the Royal Danish Theatre hosted a birthday performance for Isabella at the theatre's Old Stage featuring performances from the field of ballet, theatre, music and opera.
Youths between the age of 17 and 24 from across the kingdom were eligible to apply for tickets to the performance which was also attended by her parents and three siblings; her grandmother, Queen Margrethe II; her cousins, Count Nikolai and Count Felix of Monpezat; her great-aunts, Princess Benedikte of Denmark and Queen Anne-Marie of Greece; as well as the Prince and Princess of Sayn-Wittgenstein-Berleburg.


Titles, styles, and honours

Isabella was originally styled "Her Royal Highness Princess Isabella of Denmark".
Since 29 April 2008, she has been styled 
"Her Royal Highness Princess Isabella of Denmark, Countess of Monpezat".



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
  AssignClass (3b3b45a3-c521-4b30-9bbf-6b8440b59af8)
 Call ID: 3b3b45a3-c521-4b30-9bbf-6b8440b59af8
  Args:
    source: Isabella_of_Denmark
    type: :Person
  AssignClass (6c3e7295-e774-4141-9242-1c4e78be63b9)
 Call ID: 6c3e7295-e774-4141-9242-1c4e78be63b9
  Args:
    type: :Woman
    source: Isabella_of_Denmark
  AssignClass (e061abc7-2d38-4fc9-94d9-5fa06496d150)
 Call ID: e061abc7-2d38-4fc9-94d9-5fa06496d150
  Args:
    type: :Person
    source: Frederik_X
  AssignClass (bee9ac05-2d8e-4f44-9f84-1196ee399667)
 Call ID: bee9ac05-2d8e-4f44-9f84-1196ee399667
  Args:
    source: Frederik_X
    type: :Man
  AssignClass (c2b9e92d-9a17-4870-b0be-9b124954993f)
 Call ID: c2b9e92d-9a17-4870-b0be-9b124954993f
  Args:
    type: :Person
    source: Mary
  AssignClass (2e715e4d-c976-43be-b53e-ec4659444fbc)
 Call ID: 2e715e4d-c976-43be-b53e-ec4659444fbc
  Args:
    source: Mary
    type: :Woman
  AssignClass (b278a88e-b12e-4db6-9b96-f4481135562b)
 Call ID: b278a88e-b12e-4db6-9b96-f4481135562b
  Args:
    source: Margrethe_II
    type: :Person
  AssignClass (afeb92d9-f83d-420c-8f2e-67722b448bce)
 Call ID: afeb92d9-f83d-420c-8f2e-67722b448bce
  Args:
    source: Margrethe_II
    type: :Woman
  AssignClass (60956c5d-40ca-43ec-95e4-5430928d8548)
 Call ID: 60956c5d-40ca-43ec-95e4-5430928d8548
  Args:
    source: Henrik
    type: :Person
  AssignClass (6c6d7dfd-d776-494c-8cd9-80a46511f126)
 Call ID: 6c6d7dfd-d776-494c-8cd9-80a46511f126
  Args:
    type: :Man
    source: Henrik_Prince
  AssignClass (38e2bd25-0855-421e-88d5-cdd7c980e0f4)
 Call ID: 38e2bd25-0855-421e-88d5-cdd7c980e0f4
  Args:
    source: Christian_Crown_Prince
    type: :Person
  AssignClass (076239d6-ea04-4585-ac7e-8a6929d2d683)
 Call ID: 076239d6-ea04-4585-ac7e-8a6929d2d683
  Args:
    source: Christian_Crown_Prince
    type: :Man
  AssignClass (56383508-8a7c-4963-ad74-4d7721ad8010)
 Call ID: 56383508-8a7c-4963-ad74-4d7721ad8010
  Args:
    type: :Person
    source: Vincent
  AssignClass (6183db63-a0c6-4d71-a73e-a13259fd40f7)
 Call ID: 6183db63-a0c6-4d71-a73e-a13259fd40f7
  Args:
    type: :Man
    source: Vincent
  AddLiteral (cee384cb-3dff-42c2-834d-56432b5c9af0)
 Call ID: cee384cb-3dff-42c2-834d-56432b5c9af0
  Args:
    relation: :hasBirthYear
    literal_value: 2007
    literal_type: xsd:integer
    source: Isabella_of_Denmark
  AddTriple (c20e3a6d-d885-4559-91c6-53bcd4068044)
 Call ID: c20e3a6d-d885-4559-91c6-53bcd4068044
  Args:
    relation: :hasFather
    target: Frederik_X
    source: Isabella_of_Denmark
  AddTriple (9a14da52-5d17-4185-99a0-b08fb05a65ca)
 Call ID: 9a14da52-5d17-4185-99a0-b08fb05a65ca
  Args:
    source: Isabella_of_Denmark
    target: Mary
    relation: :hasMother
  AddTriple (d23fe5d7-d026-41d0-8a56-c12b579fb047)
 Call ID: d23fe5d7-d026-41d0-8a56-c12b579fb047
  Args:
    relation: :hasFather
    target: Henrik_Prince
    source: Frederik_X
  AddTriple (faf73a20-a341-46dd-a2f7-b6a0498821f3)
 Call ID: faf73a20-a341-46dd-a2f7-b6a0498821f3
  Args:
    relation: :hasMother
    target: Margrethe_II
    source: Frederik_X
  AddTriple (5b028fb1-dfa4-4cb0-b1eb-c892832f12e9)
 Call ID: 5b028fb1-dfa4-4cb0-b1eb-c892832f12e9
  Args:
    target: Christian_Crown_Prince
    source: Isabella_of_Denmark
    relation: :hasBrother
  AddTriple (e5003512-433a-42a9-a6ea-0579ef048662)
 Call ID: e5003512-433a-42a9-a6ea-0579ef048662
  Args:
    source: Isabella_of_Denmark
    target: Vincent
    relation: :hasBrother
  Finish (7818fe6f-6e84-4a17-a504-e6af51725dda)
 Call ID: 7818fe6f-6e84-4a17-a504-e6af51725dda
  Args: