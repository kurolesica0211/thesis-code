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
Princess Josephine of Denmark, Countess of Monpezat RE (Josephine Sophia Ivalo Mathilda; born 8 January 2011) is a member of the Danish royal family.
She is the fourth and youngest child of King Frederik X and Queen Mary, and the seventh grandchild of Queen Margrethe II and Prince Henrik.
She is the twin sister of Prince Vincent.
Josephine is fourth in line to the Danish throne, after her older siblings, Crown Prince Christian and Princess Isabella, and her elder twin brother, Prince Vincent.
Birth and christening

Queen Margrethe II


Josephine was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:56 am local time, 26 minutes after her twin brother.
Josephine and Vincent were baptised on 14 April at the Church of Holmen in central Copenhagen by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Princess Josephine wore a christening gown found among her great-grandmother Queen Ingrid's belongings, making her the first child of a future Danish monarch not to wear the Danish royal family's traditional christening gown (which was worn by her twin brother) since it was taken into use in 1870.
The Princess's name was announced as Josephine Sophia Ivalo Mathilda.
Her godparents are her paternal aunt, Princess Marie of Denmark; her maternal aunt, Patricia Bailey; as well as her parents' friends Prince Carlo, Duke of Castro, Count Bendt Wedell, Birgitte Handwerk and Josephine Rechner.
Public appearances and education

On 3 August 2014, during the family's official visit to Greenland, Josephine, her parents and siblings, took part in a tree planting in Qaqortoq's new poplar grove, Ivalos og Miniks Poppellund, named after Josephine and her brother who are known by their Greenlandic middle names in Greenland.
On 15 August 2017, Josephine and her twin brother started school at Tranegårdsskolen in Gentofte – the same public school as her older siblings.
In August 2023, the Royal House announced that Josephine would be starting at Kildegård Privatskole in Hellerup in September 2023.
Both Josephine and her twin brother were confirmed on 18 April 2026.
Titles, styles, and honours

Josephine is styled as Her Royal Highness Princess Josephine of Denmark, Countess of Monpezat.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e7413d2f-66fa-44d7-814c-91ac24293714)
 Call ID: e7413d2f-66fa-44d7-814c-91ac24293714
  Args:
    source: :Josephine_of_Denmark
    type: :Person
  AssignClass (3cca8b71-f8c5-407f-af15-58e6dee27df3)
 Call ID: 3cca8b71-f8c5-407f-af15-58e6dee27df3
  Args:
    source: :Josephine_of_Denmark
    type: :Woman
  AssignClass (a33ab72f-5cbe-4353-aac1-fe6cf896b599)
 Call ID: a33ab72f-5cbe-4353-aac1-fe6cf896b599
  Args:
    type: :Person
    source: :Frederik_X
  AssignClass (ac9d3906-4538-49af-9129-1e4c686b8a3c)
 Call ID: ac9d3906-4538-49af-9129-1e4c686b8a3c
  Args:
    type: :Man
    source: :Frederik_X
  AssignClass (91ed6317-421a-431e-baea-a897421d1ab8)
 Call ID: 91ed6317-421a-431e-baea-a897421d1ab8
  Args:
    type: :Person
    source: :Mary_of_Denmark
  AssignClass (cce304e5-3f15-4927-9976-584d34800651)
 Call ID: cce304e5-3f15-4927-9976-584d34800651
  Args:
    source: :Mary_of_Denmark
    type: :Woman
  AssignClass (eabd0500-8621-4390-9a76-aa9f1932cc16)
 Call ID: eabd0500-8621-4390-9a76-aa9f1932cc16
  Args:
    source: :Margrethe_II
    type: :Person
  AssignClass (2d58d198-cac9-42c7-8c31-0190906ce75c)
 Call ID: 2d58d198-cac9-42c7-8c31-0190906ce75c
  Args:
    source: :Margrethe_II
    type: :Woman
  AssignClass (e6ddc97a-188b-4eb8-aaff-435f9850dd1c)
 Call ID: e6ddc97a-188b-4eb8-aaff-435f9850dd1c
  Args:
    source: :Henrik_of_Denmark
    type: :Person
  AssignClass (bd7846c5-ee8e-4121-8bb2-01e976051151)
 Call ID: bd7846c5-ee8e-4121-8bb2-01e976051151
  Args:
    type: :Man
    source: :Henrik_of_Denmark
  AssignClass (ea823002-1366-4f37-9e94-fa98883b1da7)
 Call ID: ea823002-1366-4f37-9e94-fa98883b1da7
  Args:
    source: :Vincent_of_Denmark
    type: :Person
  AssignClass (71aa33bb-36a4-4abf-bcad-c89af2f131c6)
 Call ID: 71aa33bb-36a4-4abf-bcad-c89af2f131c6
  Args:
    type: :Man
    source: :Vincent_of_Denmark
  AssignClass (bb25f8d4-4865-4709-9f8d-c04d94f3c4d7)
 Call ID: bb25f8d4-4865-4709-9f8d-c04d94f3c4d7
  Args:
    type: :Person
    source: :Christian_of_Denmark
  AssignClass (f323fd25-a5ef-4f34-b701-e8aaf657c49d)
 Call ID: f323fd25-a5ef-4f34-b701-e8aaf657c49d
  Args:
    source: :Christian_of_Denmark
    type: :Man
  AssignClass (7c128a7a-07eb-43df-b0e4-ebacacd62a33)
 Call ID: 7c128a7a-07eb-43df-b0e4-ebacacd62a33
  Args:
    type: :Person
    source: :Isabella_of_Denmark
  AssignClass (ca6f68b7-e9ab-4294-8534-34c0a7dd1e14)
 Call ID: ca6f68b7-e9ab-4294-8534-34c0a7dd1e14
  Args:
    type: :Woman
    source: :Isabella_of_Denmark
  AssignClass (a1fdf608-18f7-4b93-a70f-e850d36ff626)
 Call ID: a1fdf608-18f7-4b93-a70f-e850d36ff626
  Args:
    type: :Person
    source: :Ingrid_of_Denmark
  AssignClass (76376ebc-82e6-4631-acdc-fc777438f570)
 Call ID: 76376ebc-82e6-4631-acdc-fc777438f570
  Args:
    source: :Ingrid_of_Denmark
    type: :Woman
  AddLiteral (12a35c5d-a26e-4a61-bf1b-1e60b8449f57)
 Call ID: 12a35c5d-a26e-4a61-bf1b-1e60b8449f57
  Args:
    relation: :hasBirthYear
    literal_value: 2011
    literal_type: xsd:positiveInteger
    source: :Josephine_of_Denmark
  AddTriple (e01c90cc-8348-49e3-ad12-9297cdfb8e5f)
 Call ID: e01c90cc-8348-49e3-ad12-9297cdfb8e5f
  Args:
    relation: :hasFather
    source: :Josephine_of_Denmark
    target: :Frederik_X
  AddTriple (f4689949-ef7c-4dbe-99ae-191754323f4a)
 Call ID: f4689949-ef7c-4dbe-99ae-191754323f4a
  Args:
    relation: :hasMother
    target: :Mary_of_Denmark
    source: :Josephine_of_Denmark
  AddTriple (4af1d730-e744-41dc-91e0-08f529b3bc36)
 Call ID: 4af1d730-e744-41dc-91e0-08f529b3bc36
  Args:
    relation: :hasSister
    source: :Josephine_of_Denmark
    target: :Isabella_of_Denmark
  AddTriple (afc6f199-093e-4e9a-87d8-6ca07f6153d2)
 Call ID: afc6f199-093e-4e9a-87d8-6ca07f6153d2
  Args:
    target: :Vincent_of_Denmark
    source: :Josephine_of_Denmark
    relation: :hasBrother
  AddTriple (4da17659-ca89-4a55-9a54-7994961b8364)
 Call ID: 4da17659-ca89-4a55-9a54-7994961b8364
  Args:
    source: :Josephine_of_Denmark
    target: :Christian_of_Denmark
    relation: :hasBrother
  AddTriple (11018372-1444-4da8-9a2c-54d9c42da18c)
 Call ID: 11018372-1444-4da8-9a2c-54d9c42da18c
  Args:
    target: :Margrethe_II
    source: :Frederik_X
    relation: :isChildOf
  AddTriple (3d4fd3f8-a6ec-49a7-8cc8-42d2da06bac5)
 Call ID: 3d4fd3f8-a6ec-49a7-8cc8-42d2da06bac5
  Args:
    target: :Henrik_of_Denmark
    source: :Frederik_X
    relation: :hasFather
  AddTriple (f04a2f72-939c-452a-9a77-515b94acf8e4)
 Call ID: f04a2f72-939c-452a-9a77-515b94acf8e4
  Args:
    relation: :hasMother
    source: :Frederik_X
    target: :Margrethe_II
  AddTriple (3a610293-0b26-4b29-ab2c-cb96bfdc803f)
 Call ID: 3a610293-0b26-4b29-ab2c-cb96bfdc803f
  Args:
    relation: :hasMother
    target: :Ingrid_of_Denmark
    source: :Josephine_of_Denmark
  RemoveTriple (af6746ba-035a-46d9-a9c6-892ed5bc26e7)
 Call ID: af6746ba-035a-46d9-a9c6-892ed5bc26e7
  Args:
    relation: :hasMother
    source: :Josephine_of_Denmark
    target: :Ingrid_of_Denmark
  AddTriple (0603bc2c-6add-4803-961a-d0a7509794d4)
 Call ID: 0603bc2c-6add-4803-961a-d0a7509794d4
  Args:
    relation: :hasAncestor
    target: :Ingrid_of_Denmark
    source: :Josephine_of_Denmark
  Finish (e82f47f2-796d-4be2-8077-6327c44feac8)
 Call ID: e82f47f2-796d-4be2-8077-6327c44feac8
  Args: