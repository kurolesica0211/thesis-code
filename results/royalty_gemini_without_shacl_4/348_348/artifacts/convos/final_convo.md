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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Jaime Bernardo of Bourbon-Parma, Count of Bardi (born 13 October 1972) is a Dutch diplomat and the second son and third child of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
He is a member of the House of Bourbon-Parma as well a member of the extended Dutch royal family.
He was the senior advisor on private sector partnerships at the United Nations High Commissioner for Refugees until 2021 and served as the climate envoy of the Netherlands.
Early life

Jaime was born in Nijmegen, Netherlands.
He has a twin sister, Princess Margarita, who was born one minute earlier.
Besides his twin sister, the prince has one elder brother, Carlos, Duke of Parma, and one younger sister, Princess Carolina.
Prince Jaime was born six weeks prematurely and stayed with his sister in an incubator at the hospital.
Jaime was baptised by Bernardus Johannes Cardinal Alfrink, with his grandfather Prince Bernhard of Lippe-Biesterfeld and his grandmother Princess Madeleine of Bourbon-Parma as his godparents.
Together with his mother and his siblings he moved to the Soestdijk Palace (Baarn), then residence of his grandparents, Queen Juliana and Prince Bernhard, where he lived for several years.
He now works for the Ministry of Foreign Affairs of the Netherlands.
His first role was as the first secretary of the Netherlands Embassy in Baghdad, before becoming a political advisor to the peace mission in Pol-e Khomri in the Baghlan Province in the northern part of Afghanistan.
Until the summer of 2007 the prince worked on secondment in the cabinet of the European Commissioner Neelie Kroes.
On 7 February 2014, the Ministry of Foreign Affairs announced that he would be appointed as ambassador of the Kingdom of the Netherlands to the Holy See.
Prince Jaime was, on 15 July 2014, sworn in as ambassador by King Willem-Alexander and he served till August 2018.
In August 2021 he started as the Climate Envoy of the Netherlands and served for over four years.
The prince performs representative tasks for the Ducal House of Bourbon-Parma.
On 9 November 2015, it was announced that the couple were expecting a second child; daughter Gloria Irene was born on (2016-05-09)9 May 2016.
In a 2015 interview, Princess Viktória stated that the gender of her future child did not matter ("fortunately, we can not influence nature in the terms of gender"), after being told that there were no grandsons for the late Duke of Parma (in April 2016, Jaime's elder brother Carlos, Duke of Parma finally had a son, named Carlos Enrique).
Titles, styles and honours

Titles

Honours

Dynastic honours

Foreign honours

Notes

Already a ducal prince from birth, his father bestowed the substantive title Conte di Bardi ('Count of Bardi') upon him on 2 September 1996.
In 1996 he was incorporated into the Dutch nobility by Queen Beatrix, with the highest noble title Prins de Bourbon de Parme (Prince of Bourbon-Parma), and styled Zijne Koninklijke Hoogheid ('His Royal Highness').
He does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a grandson of Queen Juliana and cousin of the present King Willem-Alexander, he is an official member of the more extended Dutch royal family.
References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (0cdc75b8-04a8-4c52-9627-7e9acb24cf4d)
 Call ID: 0cdc75b8-04a8-4c52-9627-7e9acb24cf4d
  Args:
    type: :Man
    source: PrinceJaimeBernardoOfBourbonParma
  AssignClass (487c062e-6507-4885-89c8-adb4fe7a1481)
 Call ID: 487c062e-6507-4885-89c8-adb4fe7a1481
  Args:
    type: :Person
    source: PrinceJaimeBernardoOfBourbonParma
  AddLiteral (629083a6-cd9e-4539-adb3-943c45ccfa19)
 Call ID: 629083a6-cd9e-4539-adb3-943c45ccfa19
  Args:
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1972
  AssignClass (f77d510d-d2fb-4436-81af-5ba06337695a)
 Call ID: f77d510d-d2fb-4436-81af-5ba06337695a
  Args:
    type: :Woman
    source: PrincessIreneOfTheNetherlands
  AssignClass (a7cef0da-359e-4800-9d1f-31657569edc8)
 Call ID: a7cef0da-359e-4800-9d1f-31657569edc8
  Args:
    type: :Person
    source: PrincessIreneOfTheNetherlands
  AssignClass (e07e3d8d-563e-4ffa-8243-5c05cf0d5539)
 Call ID: e07e3d8d-563e-4ffa-8243-5c05cf0d5539
  Args:
    type: :Man
    source: CarlosHugoDukeOfParma
  AssignClass (8222f612-002c-4f7a-b5e8-c8572ee66290)
 Call ID: 8222f612-002c-4f7a-b5e8-c8572ee66290
  Args:
    type: :Person
    source: CarlosHugoDukeOfParma
  AddTriple (43c49d12-fbdd-4848-b269-a7113260d46e)
 Call ID: 43c49d12-fbdd-4848-b269-a7113260d46e
  Args:
    target: PrincessIreneOfTheNetherlands
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :hasMother
  AddTriple (3818e039-b1f3-4903-b5ed-d820eeb0a936)
 Call ID: 3818e039-b1f3-4903-b5ed-d820eeb0a936
  Args:
    target: CarlosHugoDukeOfParma
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :hasFather
  AssignClass (4a17ac90-7e99-421a-83ae-09e20fd4c899)
 Call ID: 4a17ac90-7e99-421a-83ae-09e20fd4c899
  Args:
    type: :Woman
    source: PrincessMargarita
  AssignClass (871cf4e0-a045-45a5-b5ee-de767ef7d360)
 Call ID: 871cf4e0-a045-45a5-b5ee-de767ef7d360
  Args:
    type: :Person
    source: PrincessMargarita
  AddTriple (fd0d4f92-e638-40ce-abbe-95116d9ed9ef)
 Call ID: fd0d4f92-e638-40ce-abbe-95116d9ed9ef
  Args:
    target: PrincessMargarita
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :isSiblingOf
  AssignClass (a2897c0d-cedc-4013-9858-0d9391bbb740)
 Call ID: a2897c0d-cedc-4013-9858-0d9391bbb740
  Args:
    type: :Man
    source: CarlosDukeOfParma
  AssignClass (1f166f37-5267-49ec-b996-167062f0b203)
 Call ID: 1f166f37-5267-49ec-b996-167062f0b203
  Args:
    type: :Person
    source: CarlosDukeOfParma
  AddTriple (fb01b012-c3c5-4f9d-867f-00870f4cca5f)
 Call ID: fb01b012-c3c5-4f9d-867f-00870f4cca5f
  Args:
    source: PrinceJaimeBernardoOfBourbonParma
    target: CarlosDukeOfParma
    relation: :isSiblingOf
  AssignClass (35a350bb-93f8-4959-b0db-2bfecf91e466)
 Call ID: 35a350bb-93f8-4959-b0db-2bfecf91e466
  Args:
    type: :Woman
    source: PrincessCarolina
  AssignClass (a04f6498-10e8-4183-b820-110bbd8a0ddb)
 Call ID: a04f6498-10e8-4183-b820-110bbd8a0ddb
  Args:
    type: :Person
    source: PrincessCarolina
  AddTriple (6ba4808f-3412-4a62-a98c-38d09dd6c903)
 Call ID: 6ba4808f-3412-4a62-a98c-38d09dd6c903
  Args:
    relation: :isSiblingOf
    source: PrinceJaimeBernardoOfBourbonParma
    target: PrincessCarolina
  AssignClass (270bc9fa-777d-49b0-a5b1-237a1f36510c)
 Call ID: 270bc9fa-777d-49b0-a5b1-237a1f36510c
  Args:
    type: :Woman
    source: GloriaIrene
  AssignClass (3e4a6410-5b13-4bea-8e15-32cd4b0301bb)
 Call ID: 3e4a6410-5b13-4bea-8e15-32cd4b0301bb
  Args:
    type: :Person
    source: GloriaIrene
  AddTriple (5b96245b-fd8d-432d-bc66-f5233c6ee751)
 Call ID: 5b96245b-fd8d-432d-bc66-f5233c6ee751
  Args:
    relation: :isChildOf
    target: PrinceJaimeBernardoOfBourbonParma
    source: GloriaIrene
  AssignClass (f595d770-149e-44cd-8666-befd11b3a020)
 Call ID: f595d770-149e-44cd-8666-befd11b3a020
  Args:
    type: :Man
    source: CarlosEnrique
  AssignClass (cb997bb7-d56f-4c81-9e23-cbb14dca6d11)
 Call ID: cb997bb7-d56f-4c81-9e23-cbb14dca6d11
  Args:
    type: :Person
    source: CarlosEnrique
  AddTriple (124034cf-aff5-41e3-b3ca-a299e4e55f83)
 Call ID: 124034cf-aff5-41e3-b3ca-a299e4e55f83
  Args:
    relation: :isChildOf
    target: CarlosDukeOfParma
    source: CarlosEnrique
  AssignClass (b969c6b3-aa41-4541-b91f-a1eae85fccde)
 Call ID: b969c6b3-aa41-4541-b91f-a1eae85fccde
  Args:
    type: :Woman
    source: PrincessViktoria
  AssignClass (22e65057-b9ad-4981-83bb-2f4b053a1d7f)
 Call ID: 22e65057-b9ad-4981-83bb-2f4b053a1d7f
  Args:
    type: :Person
    source: PrincessViktoria
  AssignClass (1104b2d4-8645-41c8-a425-fa59677292e5)
 Call ID: 1104b2d4-8645-41c8-a425-fa59677292e5
  Args:
    type: :Woman
    source: PrincessJoan
  AssignClass (f3ec728f-b9f9-49d2-94da-f48f018cc7f6)
 Call ID: f3ec728f-b9f9-49d2-94da-f48f018cc7f6
  Args:
    type: :Person
    source: PrincessJoan
  AssignClass (66db5c8c-42ca-461b-9749-e4a1bb1d4c82)
 Call ID: 66db5c8c-42ca-461b-9749-e4a1bb1d4c82
  Args:
    type: :Woman
    source: PrincessMariaPia
  AssignClass (e993e00c-bf52-4e23-ae1e-8ceffe5f9190)
 Call ID: e993e00c-bf52-4e23-ae1e-8ceffe5f9190
  Args:
    type: :Person
    source: PrincessMariaPia
  AssignClass (825aa55c-8c5d-4643-84c9-2c3662098aa7)
 Call ID: 825aa55c-8c5d-4643-84c9-2c3662098aa7
  Args:
    type: :Woman
    source: PrincessMarina
  AssignClass (2b785b7a-cbb2-41e2-b5bf-2e519e76aec6)
 Call ID: 2b785b7a-cbb2-41e2-b5bf-2e519e76aec6
  Args:
    type: :Person
    source: PrincessMarina
  AssignClass (44a19a51-2059-419f-b0fa-bdf109641bbb)
 Call ID: 44a19a51-2059-419f-b0fa-bdf109641bbb
  Args:
    type: :Man
    source: PrinceRemy
  AssignClass (8603e595-f81d-4465-8f49-d6a9a0a60a00)
 Call ID: 8603e595-f81d-4465-8f49-d6a9a0a60a00
  Args:
    type: :Person
    source: PrinceRemy
  AssignClass (4888c85f-41c1-4f53-a97f-f238c886c572)
 Call ID: 4888c85f-41c1-4f53-a97f-f238c886c572
  Args:
    type: :Woman
    source: PrincessElisabeth
  AssignClass (079a6757-2804-4b61-b935-767207117917)
 Call ID: 079a6757-2804-4b61-b935-767207117917
  Args:
    type: :Person
    source: PrincessElisabeth
  AssignClass (c53b56d8-07cf-4d0e-9160-707945f4fd44)
 Call ID: c53b56d8-07cf-4d0e-9160-707945f4fd44
  Args:
    type: :Woman
    source: PrincessChantal
  AssignClass (597f4ef3-a8a1-4362-9cc4-f838ca4f658c)
 Call ID: 597f4ef3-a8a1-4362-9cc4-f838ca4f658c
  Args:
    type: :Person
    source: PrincessChantal
  AssignClass (a0e6b999-4267-4f34-b6ad-bf6b69d45b33)
 Call ID: a0e6b999-4267-4f34-b6ad-bf6b69d45b33
  Args:
    type: :Man
    source: PrinceJean
  AssignClass (14e5f435-90be-43f3-a50c-0302efb41a02)
 Call ID: 14e5f435-90be-43f3-a50c-0302efb41a02
  Args:
    type: :Person
    source: PrinceJean
  AssignClass (5b096cab-8f0b-4483-a971-33d2f87bb631)
 Call ID: 5b096cab-8f0b-4483-a971-33d2f87bb631
  Args:
    type: :Woman
    source: PrincessVirginia
  AssignClass (faeaaf76-4450-45c2-8c27-660cd0ee3e2c)
 Call ID: faeaaf76-4450-45c2-8c27-660cd0ee3e2c
  Args:
    type: :Person
    source: PrincessVirginia
  AssignClass (c49b2b54-5dbe-4e0e-a30a-8b319f935f01)
 Call ID: c49b2b54-5dbe-4e0e-a30a-8b319f935f01
  Args:
    type: :Woman
    source: PrincessBeatrix
  AssignClass (69272d26-7cf2-4c3c-beca-38fd9de2510c)
 Call ID: 69272d26-7cf2-4c3c-beca-38fd9de2510c
  Args:
    type: :Person
    source: PrincessBeatrix
  AssignClass (9795f92d-1edb-49ca-855a-4fa61f4f846d)
 Call ID: 9795f92d-1edb-49ca-855a-4fa61f4f846d
  Args:
    type: :Woman
    source: PrincessMargriet
  AssignClass (ccc3ced0-b82b-4c84-bcc7-2546f2848e00)
 Call ID: ccc3ced0-b82b-4c84-bcc7-2546f2848e00
  Args:
    type: :Person
    source: PrincessMargriet
  AssignClass (975dce75-9d6d-4cfb-ab6d-3aa1501019be)
 Call ID: 975dce75-9d6d-4cfb-ab6d-3aa1501019be
  Args:
    type: :Man
    source: PieterVanVollenhoven
  AssignClass (ade3d6ef-5142-4048-8bca-fd1815890a52)
 Call ID: ade3d6ef-5142-4048-8bca-fd1815890a52
  Args:
    type: :Person
    source: PieterVanVollenhoven
  Finish (d0e62ab4-87fb-4b9e-903f-5c3bd2c62898)
 Call ID: d0e62ab4-87fb-4b9e-903f-5c3bd2c62898
  Args: