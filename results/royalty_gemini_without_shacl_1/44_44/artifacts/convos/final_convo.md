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
  AssignClass (dafebf83-ea60-4df0-bc5e-383cab05236f)
 Call ID: dafebf83-ea60-4df0-bc5e-383cab05236f
  Args:
    type: :Person
    source: :Isabella_of_Denmark
  AssignClass (d8a0fdb4-d582-4ee4-a237-90118236efe2)
 Call ID: d8a0fdb4-d582-4ee4-a237-90118236efe2
  Args:
    type: :Woman
    source: :Isabella_of_Denmark
  AddLiteral (f4779447-0abf-46b1-8ca6-0a4d25a6077a)
 Call ID: f4779447-0abf-46b1-8ca6-0a4d25a6077a
  Args:
    literal_value: 2007
    source: :Isabella_of_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (2c0b1f22-4abe-48ca-84d2-2ca165918994)
 Call ID: 2c0b1f22-4abe-48ca-84d2-2ca165918994
  Args:
    source: :Frederik_X
    type: :Person
  AssignClass (4ad21514-007b-400c-913c-7e7ee3ce1358)
 Call ID: 4ad21514-007b-400c-913c-7e7ee3ce1358
  Args:
    source: :Frederik_X
    type: :Man
  AssignClass (9bc9bd8c-7f20-4a87-977d-d21a23831cb5)
 Call ID: 9bc9bd8c-7f20-4a87-977d-d21a23831cb5
  Args:
    source: :Mary
    type: :Person
  AssignClass (a6b906af-4e02-424a-8f40-6a61526d1e63)
 Call ID: a6b906af-4e02-424a-8f40-6a61526d1e63
  Args:
    source: :Mary
    type: :Woman
  AddTriple (a8f6fb11-f8bf-4f06-bed7-3b504dba8b1e)
 Call ID: a8f6fb11-f8bf-4f06-bed7-3b504dba8b1e
  Args:
    source: :Isabella_of_Denmark
    relation: :hasFather
    target: :Frederik_X
  AddTriple (8dfe0120-5ea0-4a9f-a2a3-b7fcf384f57d)
 Call ID: 8dfe0120-5ea0-4a9f-a2a3-b7fcf384f57d
  Args:
    target: :Mary
    source: :Isabella_of_Denmark
    relation: :hasMother
  AssignClass (9db1bdf1-8ddb-421d-ba89-3be30f5f35b1)
 Call ID: 9db1bdf1-8ddb-421d-ba89-3be30f5f35b1
  Args:
    source: :Margrethe_II
    type: :Person
  AssignClass (29350224-2a9c-4149-8f43-720372407695)
 Call ID: 29350224-2a9c-4149-8f43-720372407695
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (db1d69a4-2661-4bbe-8802-0f1a3d2f0360)
 Call ID: db1d69a4-2661-4bbe-8802-0f1a3d2f0360
  Args:
    type: :Person
    source: :Henrik
  AssignClass (766d90ed-8dbb-4a87-9411-043a8c204629)
 Call ID: 766d90ed-8dbb-4a87-9411-043a8c204629
  Args:
    type: :Man
    source: :Henrik
  AddTriple (1e737ee5-b0f1-407f-add1-a8bb181dc64b)
 Call ID: 1e737ee5-b0f1-407f-add1-a8bb181dc64b
  Args:
    target: :Margrethe_II
    source: :Frederik_X
    relation: :hasParent
  AddTriple (448f44ff-5629-4b91-b044-fd1cb0415ad9)
 Call ID: 448f44ff-5629-4b91-b044-fd1cb0415ad9
  Args:
    source: :Frederik_X
    relation: :hasParent
    target: :Henrik
  AssignClass (d37acd1a-7826-488c-b1bf-37e3a851cf4e)
 Call ID: d37acd1a-7826-488c-b1bf-37e3a851cf4e
  Args:
    type: :Person
    source: :Christian_of_Denmark
  AssignClass (564e691d-bb8c-4a7a-b454-44a2c4028dfa)
 Call ID: 564e691d-bb8c-4a7a-b454-44a2c4028dfa
  Args:
    type: :Man
    source: :Christian_of_Denmark
  AddTriple (8360260f-02d9-4e75-b9ad-c299aa5a08a5)
 Call ID: 8360260f-02d9-4e75-b9ad-c299aa5a08a5
  Args:
    target: :Christian_of_Denmark
    relation: :hasBrother
    source: :Isabella_of_Denmark
  AssignClass (2eed8cea-f566-443c-95fc-f7789a9b3a79)
 Call ID: 2eed8cea-f566-443c-95fc-f7789a9b3a79
  Args:
    type: :Person
    source: :Vincent_of_Denmark
  AssignClass (e6023002-0868-424c-930b-531f75a0835b)
 Call ID: e6023002-0868-424c-930b-531f75a0835b
  Args:
    type: :Man
    source: :Vincent_of_Denmark
  AddTriple (271af10c-06e7-48a3-a41a-938b0ccf1ba9)
 Call ID: 271af10c-06e7-48a3-a41a-938b0ccf1ba9
  Args:
    source: :Isabella_of_Denmark
    relation: :hasBrother
    target: :Vincent_of_Denmark
  Finish (d3166eb0-07f9-4f32-956a-252037b60c8e)
 Call ID: d3166eb0-07f9-4f32-956a-252037b60c8e
  Args: