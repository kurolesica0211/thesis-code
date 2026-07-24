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
  AssignClass (5200df84-4ca3-4585-bb8f-39492ffaea42)
 Call ID: 5200df84-4ca3-4585-bb8f-39492ffaea42
  Args:
    type: :Woman
    source: :Isabella_of_Denmark
  AssignClass (2001aab7-0108-4301-acd1-dfd38de17e58)
 Call ID: 2001aab7-0108-4301-acd1-dfd38de17e58
  Args:
    source: :Isabella_of_Denmark
    type: :Person
  AssignClass (30ac0667-327c-4cdd-9fc0-068c8c3b1e11)
 Call ID: 30ac0667-327c-4cdd-9fc0-068c8c3b1e11
  Args:
    source: :Frederik_X
    type: :Man
  AssignClass (ccca3eca-596a-470f-8b40-3e1c4519d656)
 Call ID: ccca3eca-596a-470f-8b40-3e1c4519d656
  Args:
    type: :Person
    source: :Frederik_X
  AssignClass (8edc4bc7-73ae-4801-b3ce-90472a8ea4e9)
 Call ID: 8edc4bc7-73ae-4801-b3ce-90472a8ea4e9
  Args:
    type: :Woman
    source: :Mary_of_Denmark
  AssignClass (8ece69d0-e157-4959-ac8a-032fdfeacdda)
 Call ID: 8ece69d0-e157-4959-ac8a-032fdfeacdda
  Args:
    type: :Person
    source: :Mary_of_Denmark
  AssignClass (367a4c09-58b6-4041-9524-404170f1c39d)
 Call ID: 367a4c09-58b6-4041-9524-404170f1c39d
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (00f85313-56db-4c29-9b38-206717b8e436)
 Call ID: 00f85313-56db-4c29-9b38-206717b8e436
  Args:
    type: :Person
    source: :Margrethe_II
  AssignClass (17dd8625-a09a-4d65-b0dd-5735cd10f7d8)
 Call ID: 17dd8625-a09a-4d65-b0dd-5735cd10f7d8
  Args:
    type: :Man
    source: :Henrik_of_Denmark
  AssignClass (3aaf0972-02d8-438a-8eda-f8ff6123600f)
 Call ID: 3aaf0972-02d8-438a-8eda-f8ff6123600f
  Args:
    type: :Person
    source: :Henrik_of_Denmark
  AssignClass (2c62247a-ec35-4ea5-a82e-00c084a434e7)
 Call ID: 2c62247a-ec35-4ea5-a82e-00c084a434e7
  Args:
    source: :Christian_of_Denmark
    type: :Man
  AssignClass (e847c325-93f4-4bd4-82c8-2c8e7472facc)
 Call ID: e847c325-93f4-4bd4-82c8-2c8e7472facc
  Args:
    source: :Christian_of_Denmark
    type: :Person
  AssignClass (3ecaab9f-619f-4a6a-9a3e-3ba75909faef)
 Call ID: 3ecaab9f-619f-4a6a-9a3e-3ba75909faef
  Args:
    type: :Man
    source: :Vincent_of_Denmark
  AssignClass (974ed703-ebb8-42be-a588-d5ad13a216f6)
 Call ID: 974ed703-ebb8-42be-a588-d5ad13a216f6
  Args:
    source: :Vincent_of_Denmark
    type: :Person
  AssignClass (4eae3909-4367-4fb7-b801-40afeda994f2)
 Call ID: 4eae3909-4367-4fb7-b801-40afeda994f2
  Args:
    type: :Man
    source: :Joachim_of_Denmark
  AssignClass (97214bb5-ce8b-4b48-9fb4-36a5c4e0ab2a)
 Call ID: 97214bb5-ce8b-4b48-9fb4-36a5c4e0ab2a
  Args:
    type: :Person
    source: :Joachim_of_Denmark
  AddLiteral (aeb4396d-2ef9-4594-97ff-28dc536ab48d)
 Call ID: aeb4396d-2ef9-4594-97ff-28dc536ab48d
  Args:
    literal_value: 2007
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: :Isabella_of_Denmark
  AddTriple (7289e242-4312-4de0-b4e6-e2d575b002a9)
 Call ID: 7289e242-4312-4de0-b4e6-e2d575b002a9
  Args:
    source: :Isabella_of_Denmark
    relation: :hasFather
    target: :Frederik_X
  AddTriple (4d60cede-fe1c-44e1-bd0e-95ec515ff00c)
 Call ID: 4d60cede-fe1c-44e1-bd0e-95ec515ff00c
  Args:
    target: :Mary_of_Denmark
    relation: :hasMother
    source: :Isabella_of_Denmark
  AddTriple (8f0f333f-7a80-4cee-b0d7-44974c0771a8)
 Call ID: 8f0f333f-7a80-4cee-b0d7-44974c0771a8
  Args:
    relation: :hasFather
    target: :Henrik_of_Denmark
    source: :Frederik_X
  AddTriple (f80ac040-24f2-47d9-8f81-f1a31eb06090)
 Call ID: f80ac040-24f2-47d9-8f81-f1a31eb06090
  Args:
    source: :Frederik_X
    target: :Margrethe_II
    relation: :hasMother
  AddTriple (30a05ab1-e4ca-40ed-9c11-36489b1ae729)
 Call ID: 30a05ab1-e4ca-40ed-9c11-36489b1ae729
  Args:
    source: :Christian_of_Denmark
    target: :Isabella_of_Denmark
    relation: :isBrotherOf
  AddTriple (7ad2b852-a225-4f67-9461-44573dddf031)
 Call ID: 7ad2b852-a225-4f67-9461-44573dddf031
  Args:
    source: :Vincent_of_Denmark
    relation: :isBrotherOf
    target: :Isabella_of_Denmark
  AddTriple (311f05a8-aee1-49ce-a82b-9f6748d1913e)
 Call ID: 311f05a8-aee1-49ce-a82b-9f6748d1913e
  Args:
    source: :Christian_of_Denmark
    target: :Frederik_X
    relation: :hasFather
  AddTriple (508b75d3-a168-48e5-83b0-b53b073259ec)
 Call ID: 508b75d3-a168-48e5-83b0-b53b073259ec
  Args:
    source: :Vincent_of_Denmark
    relation: :hasFather
    target: :Frederik_X
  AddTriple (edaac790-dd8d-4893-8de8-d071d78e0ce7)
 Call ID: edaac790-dd8d-4893-8de8-d071d78e0ce7
  Args:
    source: :Christian_of_Denmark
    target: :Mary_of_Denmark
    relation: :hasMother
  AddTriple (b37815b5-65f9-4d2e-9e69-0f88a3fe1eaa)
 Call ID: b37815b5-65f9-4d2e-9e69-0f88a3fe1eaa
  Args:
    relation: :hasMother
    target: :Mary_of_Denmark
    source: :Vincent_of_Denmark
  AddTriple (79f814cd-b85f-477e-8d52-f73cdf5f376c)
 Call ID: 79f814cd-b85f-477e-8d52-f73cdf5f376c
  Args:
    relation: :isFatherOf
    target: :Frederik_X
    source: :Henrik_of_Denmark
  AddTriple (f8796070-d33b-400e-b6ee-ba6e5a3cbca6)
 Call ID: f8796070-d33b-400e-b6ee-ba6e5a3cbca6
  Args:
    source: :Margrethe_II
    relation: :isMotherOf
    target: :Frederik_X
  Finish (60f8ffbf-01e5-4c6d-8c15-509dac747b1e)
 Call ID: 60f8ffbf-01e5-4c6d-8c15-509dac747b1e
  Args: