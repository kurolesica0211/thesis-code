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
  AssignClass (1b93be50-20b4-48c9-9093-a1c6352e625c)
 Call ID: 1b93be50-20b4-48c9-9093-a1c6352e625c
  Args:
    type: :Man
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
  AssignClass (b1e9c374-6fd3-4491-9c8f-5d11ac6cfef3)
 Call ID: b1e9c374-6fd3-4491-9c8f-5d11ac6cfef3
  Args:
    type: :Person
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
  AddLiteral (d250617e-b4a0-4ff4-a345-2a4d95ab001d)
 Call ID: d250617e-b4a0-4ff4-a345-2a4d95ab001d
  Args:
    literal_value: 1972
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (6628038b-c642-4152-9fe0-a5584dc0278d)
 Call ID: 6628038b-c642-4152-9fe0-a5584dc0278d
  Args:
    type: :Woman
    source: :Princess_Irene_of_the_Netherlands
  AssignClass (c39dd2e6-f6e5-42f8-b7f1-81937cbf305e)
 Call ID: c39dd2e6-f6e5-42f8-b7f1-81937cbf305e
  Args:
    type: :Person
    source: :Princess_Irene_of_the_Netherlands
  AssignClass (8f02b01d-e9ab-45b1-96ad-3ce56d76c1a8)
 Call ID: 8f02b01d-e9ab-45b1-96ad-3ce56d76c1a8
  Args:
    type: :Man
    source: :Carlos_Hugo_Duke_of_Parma
  AssignClass (342fc177-a731-45bb-b00e-1ff0809734e2)
 Call ID: 342fc177-a731-45bb-b00e-1ff0809734e2
  Args:
    type: :Person
    source: :Carlos_Hugo_Duke_of_Parma
  AddTriple (bbf35b65-b977-4b75-9513-33b00fa91265)
 Call ID: bbf35b65-b977-4b75-9513-33b00fa91265
  Args:
    relation: :hasMother
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
    target: :Princess_Irene_of_the_Netherlands
  AddTriple (d3e2b166-af0e-42ea-ae07-ec917542c9e8)
 Call ID: d3e2b166-af0e-42ea-ae07-ec917542c9e8
  Args:
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
    target: :Carlos_Hugo_Duke_of_Parma
    relation: :hasFather
  AssignClass (218cd25d-842d-4bb4-91a4-942a784740e9)
 Call ID: 218cd25d-842d-4bb4-91a4-942a784740e9
  Args:
    type: :Woman
    source: :Princess_Margarita
  AssignClass (a8070571-91a8-4a5d-8b6c-a64c28bff0a8)
 Call ID: a8070571-91a8-4a5d-8b6c-a64c28bff0a8
  Args:
    type: :Person
    source: :Princess_Margarita
  AddTriple (9ca8273b-1992-4030-bddb-8eac382900c6)
 Call ID: 9ca8273b-1992-4030-bddb-8eac382900c6
  Args:
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
    target: :Princess_Margarita
    relation: :isSiblingOf
  AssignClass (1b263386-920c-4551-bc09-1913bf81ac11)
 Call ID: 1b263386-920c-4551-bc09-1913bf81ac11
  Args:
    type: :Man
    source: :Carlos_Duke_of_Parma
  AssignClass (91343302-4a2d-4ce0-9f59-3ffa8d21d22e)
 Call ID: 91343302-4a2d-4ce0-9f59-3ffa8d21d22e
  Args:
    type: :Person
    source: :Carlos_Duke_of_Parma
  AddTriple (abee8597-18e6-4a4b-a045-a67df2a25d6d)
 Call ID: abee8597-18e6-4a4b-a045-a67df2a25d6d
  Args:
    relation: :isSiblingOf
    target: :Carlos_Duke_of_Parma
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
  AssignClass (df7ef5b2-20e5-4e92-bb61-37f393b4c061)
 Call ID: df7ef5b2-20e5-4e92-bb61-37f393b4c061
  Args:
    type: :Woman
    source: :Princess_Carolina
  AssignClass (dcde37d1-fd93-4831-852e-c5c3308b045e)
 Call ID: dcde37d1-fd93-4831-852e-c5c3308b045e
  Args:
    type: :Person
    source: :Princess_Carolina
  AddTriple (5326a24b-d891-4583-a481-d1a5abbf3ab6)
 Call ID: 5326a24b-d891-4583-a481-d1a5abbf3ab6
  Args:
    relation: :isSiblingOf
    source: :Prince_Jaime_Bernardo_of_Bourbon-Parma
    target: :Princess_Carolina
  AssignClass (2dff7e21-c422-44e1-b974-23779aa61ea1)
 Call ID: 2dff7e21-c422-44e1-b974-23779aa61ea1
  Args:
    type: :Man
    source: :Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (b9944cd0-56f7-4ff3-acd6-d98e4e5981b0)
 Call ID: b9944cd0-56f7-4ff3-acd6-d98e4e5981b0
  Args:
    type: :Person
    source: :Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (e4428cd6-e8fa-4cbe-ba17-c8231d206312)
 Call ID: e4428cd6-e8fa-4cbe-ba17-c8231d206312
  Args:
    type: :Woman
    source: :Princess_Madeleine_of_Bourbon-Parma
  AssignClass (29448368-afa9-477f-a898-f09f485b7c02)
 Call ID: 29448368-afa9-477f-a898-f09f485b7c02
  Args:
    type: :Person
    source: :Princess_Madeleine_of_Bourbon-Parma
  AssignClass (2dd49f87-2f36-43dd-a1af-b24b10fb3be6)
 Call ID: 2dd49f87-2f36-43dd-a1af-b24b10fb3be6
  Args:
    type: :Woman
    source: :Queen_Juliana
  AssignClass (57019652-814c-4c4a-b7f0-8f0d06ccd805)
 Call ID: 57019652-814c-4c4a-b7f0-8f0d06ccd805
  Args:
    type: :Person
    source: :Queen_Juliana
  AssignClass (8e682984-5e61-4ad6-8b13-69645d6e36e3)
 Call ID: 8e682984-5e61-4ad6-8b13-69645d6e36e3
  Args:
    type: :Woman
    source: :Gloria_Irene
  AssignClass (087a8cb2-798e-423a-a439-65a15bbb056c)
 Call ID: 087a8cb2-798e-423a-a439-65a15bbb056c
  Args:
    type: :Person
    source: :Gloria_Irene
  AddTriple (02a5921d-2f7a-4c92-b8bf-4425233a4808)
 Call ID: 02a5921d-2f7a-4c92-b8bf-4425233a4808
  Args:
    source: :Gloria_Irene
    target: :Prince_Jaime_Bernardo_of_Bourbon-Parma
    relation: :isChildOf
  AssignClass (4ba1ea08-9c27-4ee5-a412-da193b607250)
 Call ID: 4ba1ea08-9c27-4ee5-a412-da193b607250
  Args:
    type: :Man
    source: :Carlos_Enrique
  AssignClass (e198d306-2168-488c-8531-379cdb6f4a69)
 Call ID: e198d306-2168-488c-8531-379cdb6f4a69
  Args:
    type: :Person
    source: :Carlos_Enrique
  AddTriple (cb654567-5bde-454c-8fe8-c88183bc32bc)
 Call ID: cb654567-5bde-454c-8fe8-c88183bc32bc
  Args:
    relation: :isChildOf
    target: :Carlos_Duke_of_Parma
    source: :Carlos_Enrique
  Finish (e3a152db-328e-456c-a22c-fa0aa4983d42)
 Call ID: e3a152db-328e-456c-a22c-fa0aa4983d42
  Args: