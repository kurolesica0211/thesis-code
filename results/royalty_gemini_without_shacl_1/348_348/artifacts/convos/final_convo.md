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
  AssignClass (12fc2b79-137c-43c1-a4cf-2a7e7b07236a)
 Call ID: 12fc2b79-137c-43c1-a4cf-2a7e7b07236a
  Args:
    source: PrinceJaimeBernardoOfBourbonParma
    type: :Man
  AssignClass (3b4d3172-17ce-4a0a-88a5-9a96749bfab2)
 Call ID: 3b4d3172-17ce-4a0a-88a5-9a96749bfab2
  Args:
    type: :Person
    source: PrinceJaimeBernardoOfBourbonParma
  AssignClass (c57726c3-c8b5-4f49-89b2-f210c455377c)
 Call ID: c57726c3-c8b5-4f49-89b2-f210c455377c
  Args:
    source: PrincessIreneOfTheNetherlands
    type: :Woman
  AssignClass (09a1fffb-af96-4429-a79e-89881067231d)
 Call ID: 09a1fffb-af96-4429-a79e-89881067231d
  Args:
    source: PrincessIreneOfTheNetherlands
    type: :Person
  AssignClass (495784f8-5abf-45e4-a8e3-91abe7d88638)
 Call ID: 495784f8-5abf-45e4-a8e3-91abe7d88638
  Args:
    type: :Man
    source: CarlosHugoDukeOfParma
  AssignClass (61638791-7c3d-4c50-bcd6-f9037f0ef8b9)
 Call ID: 61638791-7c3d-4c50-bcd6-f9037f0ef8b9
  Args:
    type: :Person
    source: CarlosHugoDukeOfParma
  AddLiteral (8f9e51e0-ffb4-4edf-889d-adeea0925a07)
 Call ID: 8f9e51e0-ffb4-4edf-889d-adeea0925a07
  Args:
    literal_type: xsd:integer
    source: PrinceJaimeBernardoOfBourbonParma
    literal_value: 1972
    relation: :hasBirthYear
  AddTriple (4618f7a3-f279-4c8d-a5ca-370e4e3c7ec4)
 Call ID: 4618f7a3-f279-4c8d-a5ca-370e4e3c7ec4
  Args:
    target: PrincessIreneOfTheNetherlands
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :hasMother
  AddTriple (ec027a95-ca0c-42b4-96d5-f430c30dee2f)
 Call ID: ec027a95-ca0c-42b4-96d5-f430c30dee2f
  Args:
    relation: :hasFather
    source: PrinceJaimeBernardoOfBourbonParma
    target: CarlosHugoDukeOfParma
  AssignClass (c204fb00-15e2-4939-ba63-1d46fc61ae22)
 Call ID: c204fb00-15e2-4939-ba63-1d46fc61ae22
  Args:
    source: PrincessMargarita
    type: :Woman
  AssignClass (99bc7129-66f7-436c-ab2f-8e5707ed0597)
 Call ID: 99bc7129-66f7-436c-ab2f-8e5707ed0597
  Args:
    source: PrincessMargarita
    type: :Person
  AddTriple (8772e558-85aa-4d55-8b6d-826e2962f2c5)
 Call ID: 8772e558-85aa-4d55-8b6d-826e2962f2c5
  Args:
    relation: :isSiblingOf
    source: PrinceJaimeBernardoOfBourbonParma
    target: PrincessMargarita
  AssignClass (b8b22ee3-2279-47e3-8a2d-bb09f6875c0a)
 Call ID: b8b22ee3-2279-47e3-8a2d-bb09f6875c0a
  Args:
    source: CarlosDukeOfParma
    type: :Man
  AssignClass (8eee2622-c3e1-42df-bfd5-b93d1120c9ec)
 Call ID: 8eee2622-c3e1-42df-bfd5-b93d1120c9ec
  Args:
    source: CarlosDukeOfParma
    type: :Person
  AddTriple (2d82fdb7-10ad-4b75-ad54-4fd23153dca7)
 Call ID: 2d82fdb7-10ad-4b75-ad54-4fd23153dca7
  Args:
    target: CarlosDukeOfParma
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :isSiblingOf
  AssignClass (1fec51ce-b30e-4a1d-a681-51ace5b94fb9)
 Call ID: 1fec51ce-b30e-4a1d-a681-51ace5b94fb9
  Args:
    source: PrincessCarolina
    type: :Woman
  AssignClass (1e6e4fb9-4b30-41d4-878a-78c96323bab0)
 Call ID: 1e6e4fb9-4b30-41d4-878a-78c96323bab0
  Args:
    source: PrincessCarolina
    type: :Person
  AddTriple (7b399739-63f0-48b2-8c50-c9ffe7419257)
 Call ID: 7b399739-63f0-48b2-8c50-c9ffe7419257
  Args:
    source: PrinceJaimeBernardoOfBourbonParma
    relation: :isSiblingOf
    target: PrincessCarolina
  AssignClass (9fa06034-7e1e-41c5-9e3c-71438d69828f)
 Call ID: 9fa06034-7e1e-41c5-9e3c-71438d69828f
  Args:
    source: GloriaIrene
    type: :Woman
  AssignClass (2bc0b1cb-6648-4fd9-923c-9bb36204700b)
 Call ID: 2bc0b1cb-6648-4fd9-923c-9bb36204700b
  Args:
    type: :Person
    source: GloriaIrene
  AddTriple (654f4080-ff84-4efb-a7e4-26487035b0b2)
 Call ID: 654f4080-ff84-4efb-a7e4-26487035b0b2
  Args:
    source: GloriaIrene
    relation: :hasFather
    target: PrinceJaimeBernardoOfBourbonParma
  AssignClass (7514f272-fe9c-4792-b323-c18f894fcc72)
 Call ID: 7514f272-fe9c-4792-b323-c18f894fcc72
  Args:
    source: PrincessViktoría
    type: :Woman
  AssignClass (48e33df6-dc02-4c4e-8993-c4a46e4057d8)
 Call ID: 48e33df6-dc02-4c4e-8993-c4a46e4057d8
  Args:
    source: PrincessViktoría
    type: :Person
  AddTriple (7ed1bddd-631c-4599-a993-98e04be373c5)
 Call ID: 7ed1bddd-631c-4599-a993-98e04be373c5
  Args:
    relation: :hasMother
    source: GloriaIrene
    target: PrincessViktoría
  AssignClass (0d65f59d-9206-4b6f-b2d2-c783a4ae7276)
 Call ID: 0d65f59d-9206-4b6f-b2d2-c783a4ae7276
  Args:
    type: :Man
    source: CarlosEnrique
  AssignClass (9cdfc9c0-5646-4360-827a-c30bd9ed9096)
 Call ID: 9cdfc9c0-5646-4360-827a-c30bd9ed9096
  Args:
    source: CarlosEnrique
    type: :Person
  AddTriple (7f6446b7-cd44-4a30-b1ea-9ee515b7c4f6)
 Call ID: 7f6446b7-cd44-4a30-b1ea-9ee515b7c4f6
  Args:
    relation: :hasFather
    source: CarlosEnrique
    target: CarlosDukeOfParma
  Finish (840e5b7f-7130-4f3c-9c54-81211bd95033)
 Call ID: 840e5b7f-7130-4f3c-9c54-81211bd95033
  Args: